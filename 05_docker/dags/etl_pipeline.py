import pandas as pd
from datetime import datetime
import boto3
import io

def read_raw_csv_from_s3(bucket_name, key):
    s3 = boto3.client("s3")
    obj = s3.get_object(Bucket=bucket_name, Key=key)
    return pd.read_csv(io.BytesIO(obj['Body'].read()))

def salvar_parquet(df, caminho_s3):
    df.to_parquet(f"s3://{caminho_s3}", index=False, engine="pyarrow", storage_options={"anon": False})

def calcular_idade(data_nascimento):
    hoje = pd.Timestamp.today()
    return hoje.year - data_nascimento.year - ((hoje.month, hoje.day) < (data_nascimento.month, data_nascimento.day))

def run_etl():
    # RAW → BRONZE
    df_raw = read_raw_csv_from_s3("dncinsight-pipeline-rid211401", "raw_data.csv")
    df_bronze = df_raw.copy()
    salvar_parquet(df_bronze, "dncinsight-pipeline-rid211401/bronze/usuarios_bronze.parquet")

    # BRONZE → SILVER
    df_silver = df_bronze.dropna(subset=["id", "signup_date", "date_of_birth", "subscription_status"]).copy()
    df_silver["signup_date"] = pd.to_datetime(df_silver["signup_date"])
    df_silver["date_of_birth"] = pd.to_datetime(df_silver["date_of_birth"])
    df_silver["age"] = df_silver["date_of_birth"].apply(calcular_idade)
    df_silver["dias_desde_cadastro"] = (datetime.now() - df_silver["signup_date"]).dt.days

    def categorizar_idade(idade):
        if idade < 18:
            return "menor de idade"
        elif idade < 30:
            return "jovem adulto"
        elif idade < 60:
            return "adulto"
        else:
            return "idoso"

    df_silver["faixa_etaria"] = df_silver["age"].apply(categorizar_idade)
    salvar_parquet(df_silver, "dncinsight-pipeline-rid211401/silver/usuarios_limpos.parquet")

    # SILVER → GOLD
    df_gold = df_silver.groupby(["faixa_etaria", "subscription_status"]).agg(
        qtd_usuarios=("id", "count"),
        idade_media=("age", "mean"),
        dias_desde_cadastro_media=("dias_desde_cadastro", "mean")
    ).reset_index()

    total_por_faixa = df_gold.groupby("faixa_etaria")["qtd_usuarios"].transform("sum")
    df_gold["pct_ativos_na_faixa"] = (df_gold["qtd_usuarios"] / total_por_faixa * 100).round(2)
    salvar_parquet(df_gold, "dncinsight-pipeline-rid211401/gold/usuarios_agrupados.parquet")
