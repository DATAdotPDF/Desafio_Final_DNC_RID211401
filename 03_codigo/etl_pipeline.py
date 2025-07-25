import os
import boto3
from dotenv import load_dotenv
import pandas as pd
from io import StringIO
from datetime import datetime

# Etapa 1: Carregando variáveis de ambiente
load_dotenv()
AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")
AWS_REGION = os.getenv("AWS_REGION")
S3_BUCKET_NAME = os.getenv("S3_BUCKET_NAME")

# Etapa 2: Criando cliente S3
s3_client = boto3.client(
    "s3",
    aws_access_key_id=AWS_ACCESS_KEY_ID,
    aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
    region_name=AWS_REGION
)

# Etapa 3: Upload da camada Bronze
def upload_bronze():
    local_path = "./01_base_de_dados/raw_data.csv"
    s3_path = "bronze/raw_data.csv"

    if not os.path.exists(local_path):
        print(f"Arquivo não encontrado em: {local_path}")
        return

    try:
        s3_client.upload_file(local_path, S3_BUCKET_NAME, s3_path)
        print(f"Arquivo enviado para: s3://{S3_BUCKET_NAME}/{s3_path}")
    except Exception as e:
        print(f"Erro ao enviar para o S3:\n{e}")

# Etapa 4: Processamento da camada Silver
def process_silver():
    s3_key_bronze = "bronze/raw_data.csv"
    s3_key_silver = "silver/usuarios_limpos.csv"

    try:
        response = s3_client.get_object(Bucket=S3_BUCKET_NAME, Key=s3_key_bronze)
        raw_csv = response['Body'].read().decode('utf-8')
        df = pd.read_csv(StringIO(raw_csv))
    except Exception as e:
        print(f"Erro ao ler Bronze do S3:\n{e}")
        return

    # Limpeza de dados
    df = df.dropna(subset=['name', 'email', 'date_of_birth'])
    df = df[df['email'].str.contains('@')]

    def calcular_idade(data_nasc):
        try:
            nascimento = datetime.strptime(data_nasc, "%Y-%m-%d")
            hoje = datetime.now()
            return hoje.year - nascimento.year - ((hoje.month, hoje.day) < (nascimento.month, nascimento.day))
        except:
            return None

    df["age"] = df["date_of_birth"].apply(calcular_idade)
    df = df.dropna(subset=["age"])
    df = df[df["age"] >= 18]

    # Exporta para o S3
    csv_buffer = StringIO()
    df.to_csv(csv_buffer, index=False)
    try:
        s3_client.put_object(Bucket=S3_BUCKET_NAME, Key=s3_key_silver, Body=csv_buffer.getvalue())
        print(f"Silver enviado para: s3://{S3_BUCKET_NAME}/{s3_key_silver}")
    except Exception as e:
        print(f"Erro ao enviar Silver para o S3:\n{e}")

# Etapa 5: Processamento da camada Gold
def process_gold():
    silver_key = "silver/usuarios_limpos.csv"
    gold_key = "gold/usuarios_agrupados.csv"

    try:
        response = s3_client.get_object(Bucket=S3_BUCKET_NAME, Key=silver_key)
        raw_csv = response["Body"].read().decode("utf-8")
        df = pd.read_csv(StringIO(raw_csv))
    except Exception as e:
        print(f"Erro ao ler Silver do S3:\n{e}")
        return

    df['date_of_birth'] = pd.to_datetime(df['date_of_birth'], errors='coerce')
    df['signup_date'] = pd.to_datetime(df['signup_date'], errors='coerce')
    df['age'] = pd.to_numeric(df['age'], errors='coerce')
    df['subscription_status'] = df['subscription_status'].astype(str)

    # Faixa etária realista até 100 anos
    bins = [18, 30, 40, 50, 60, 70, 100]
    labels = ['19–30', '31–40', '41–50', '51–60', '61–70', '71+']
    df['faixa_etaria'] = pd.cut(df['age'], bins=bins, labels=labels, right=True)

    df['dias_desde_cadastro'] = (pd.Timestamp.today() - df['signup_date']).dt.days

    agrupado = df.groupby(['faixa_etaria', 'subscription_status']).agg(
        qtd_usuarios=('id', 'count'),
        idade_media=('age', 'mean'),
        dias_desde_cadastro_media=('dias_desde_cadastro', 'mean')
    ).reset_index()

    total_por_faixa = df.groupby('faixa_etaria')['id'].count().reset_index(name='total_faixa')
    ativos_por_faixa = df[df['subscription_status'] == 'active'].groupby('faixa_etaria')['id'].count().reset_index(name='qtd_ativos')

    porcentagem = pd.merge(total_por_faixa, ativos_por_faixa, on='faixa_etaria', how='left')
    porcentagem['pct_ativos_na_faixa'] = (porcentagem['qtd_ativos'] / porcentagem['total_faixa']) * 100
    porcentagem = porcentagem[['faixa_etaria', 'pct_ativos_na_faixa']]

    final = pd.merge(agrupado, porcentagem, on='faixa_etaria', how='left')
    final['idade_media'] = final['idade_media'].round(1)
    final['dias_desde_cadastro_media'] = final['dias_desde_cadastro_media'].round(1)
    final['pct_ativos_na_faixa'] = final['pct_ativos_na_faixa'].round(1)

    # Exporta camada Gold para o S3
    csv_buffer = StringIO()
    final.to_csv(csv_buffer, index=False)
    try:
        s3_client.put_object(Bucket=S3_BUCKET_NAME, Key=gold_key, Body=csv_buffer.getvalue())
        print(f"Gold enviado para: s3://{S3_BUCKET_NAME}/{gold_key}")
    except Exception as e:
        print(f"Erro ao enviar Gold para o S3:\n{e}")

# Execução completa do pipeline
if __name__ == "__main__":
    upload_bronze()
    process_silver()
    process_gold()
    print("Pipeline completo executado com sucesso.")
