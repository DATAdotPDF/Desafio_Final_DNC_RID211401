<p align="center">
  <img src="00_documentos/DESAFIO_FINAL_ENG_DADOS_BANNER.png" alt="Banner do Projeto" width="100%" />
</p>


# 🚀 Pipeline de Dados com Airflow, Python e Dash

Projeto final do curso de Engenharia de Dados da DNC, desenvolvido no macOS, com foco em automação de ETL, orquestração com Airflow via Docker, armazenamento no S3 e visualização com Plotly Dash.

## 📋 Descrição do Projeto

Este projeto simula um pipeline completo de engenharia de dados para uma empresa fictícia chamada **DncInsight Solutions**. Ele utiliza um dataset `.csv` como fonte bruta e implementa um fluxo em camadas (**Bronze**, **Silver** e **Gold**) com tratamento, enriquecimento e agregações. A camada final é exibida em um dashboard interativo.

Toda a automação foi realizada com **Python** e **Airflow**, os dados tratados são armazenados no **S3**, e o dashboard foi desenvolvido com **Plotly Dash**.

## 📁 Estrutura do Projeto
```markdown
dnc_pipeline/
├── 00_documentos/    # Documentos de apoio e visuais
├── 01_base_de_dados/ # CSVs brutos e amostras
├── 02_empresa/       # Informações fictícias e artefatos de negócio
├── 03_codigo/        # Código ETL original em Python
├── 04_dag_airflow/   # DAGs e configurações do Airflow
├── 05_docker/        # docker-compose.yml e arquivos relacionados
├── 06_dashboard/     # App com Plotly Dash
├── data/             # Parquets locais (opcional)
├── logs/             # Logs de execução do pipeline
├── venv/             # Ambiente virtual Python
├── .env              # Credenciais e variáveis do ambiente
├── start.sh          # Script de execução do pipeline
├── requirements.txt  # Dependências do projeto
└── README.md         # Este arquivo
```

## ⚙️ Tecnologias Utilizadas

- **Python 3.11**  
- **Apache Airflow** (Docker)  
- **AWS S3** (Bucket: `dncinsight-pipeline-rid211401`)  
- **pandas**, **boto3**, **pyarrow**  
- **Plotly Dash**  
- **macOS Sonoma (13.6.6)**

## 🧭 Etapas do Pipeline

1. Leitura da base bruta diretamente do S3 (camada Raw).  
2. Transformações iniciais salvas como camada Bronze.  
3. Enriquecimento e limpeza na camada Silver.  
4. Agregações e métricas de negócio na camada Gold.  
5. Visualização em tempo real com filtros dinâmicos no Dash.

## ✅ Como Executar Localmente (macOS)

```bash
# Clone o repositório
git clone https://github.com/DATAdotPDF/Desafio_Final_DNC_RID211401.git
cd dnc_pipeline

# Crie o ambiente virtual
python3 -m venv venv
source venv/bin/activate

# Instale as dependências
pip install -r requirements.txt

# Crie um arquivo .env com as variáveis:
AWS_ACCESS_KEY_ID=sua_chave
AWS_SECRET_ACCESS_KEY=sua_secret
AWS_REGION=sa-east-1
S3_BUCKET_NAME=dncinsight-pipeline-rid211401

# Execute o pipeline:
bash start.sh

# Execute o dashboard:
python 06_dashboard/app.py
```

### ☁️ Execução com Airflow (Docker)
```bash
cd 05_docker

# Inicialize o ambiente
docker-compose up airflow-init
docker-compose up
```

Acesse [http://localhost:8080](http://localhost:8080)  
**Usuário:** airflow  
**Senha:** airflow  

Execute a DAG `dnc_pipeline` manualmente pela interface.

### 📊 Dashboard
O dashboard interativo exibe:  
- Quantidade de usuários por faixa etária e status.  
- Porcentagem de usuários ativos por grupo.  
- Média de dias desde o cadastro.  
- Filtros dinâmicos por faixa etária e status.

### 📌 Observações
- Projeto desenvolvido e testado exclusivamente no macOS.  
- Comandos e permissões podem variar em Windows ou Linux.  
- Estrutura modular, preparada para deploy futuro em nuvem ou versão pública.

---

## 📚 Referências

- [DNC Escola de Dados](https://www.escoladnc.com.br)  
- [AWS S3](https://aws.amazon.com/pt/s3/)  
- [Plotly Dash](https://dash.plotly.com/)  
- [Apache Airflow](https://airflow.apache.org/)  
- [GitHub do Projeto SIDRA](https://github.com/DATAdotPDF/Desafio_Pratico_DNC_Grupo6)  

---

Desenvolvido por [Pedro Ferreira – LinkedIn](https://www.linkedin.com/in/datadotpdf)
