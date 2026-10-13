<p align="center">
  <img src="00_documentos/DESAFIO_FINAL_ENG_DADOS_BANNER.png" alt="Data Engineering Final Project Banner" width="100%" />
</p>

# 🚀 Data Pipeline with Airflow, Python, and Dash

Final project for DNC's Data Engineering course, developed on macOS. It focuses on ETL automation, Airflow orchestration through Docker, S3 storage, and Plotly Dash visualization.

## 📋 Project Description

This project simulates a complete data engineering pipeline for a fictional company called **DncInsight Solutions**. It uses a `.csv` dataset as the raw source and builds a layered flow (**Bronze**, **Silver**, and **Gold**) with cleaning, enrichment, and aggregation. The final layer is displayed in an interactive dashboard.

All automation was built with **Python** and **Airflow**. Processed data is stored in **S3**, and the dashboard was developed with **Plotly Dash**.

## 📁 Project Structure
```markdown
dnc_pipeline/
├── 00_documentos/    # Supporting documents and visuals
├── 01_base_de_dados/ # Raw CSV files and samples
├── 02_empresa/       # Fictional business information and artifacts
├── 03_codigo/        # Original Python ETL code
├── 04_dag_airflow/   # Airflow DAGs and settings
├── 05_docker/        # docker-compose.yml and related files
├── 06_dashboard/     # Plotly Dash app
├── data/             # Optional local Parquet files
├── logs/             # Pipeline execution logs
├── venv/             # Python virtual environment
├── .env              # Credentials and environment variables
├── start.sh          # Pipeline execution script
├── requirements.txt  # Project dependencies
└── README.md         # This file
```

## ⚙️ Technologies Used

- **Python 3.11**
- **Apache Airflow** with Docker
- **AWS S3** (bucket: `dncinsight-pipeline-rid211401`)
- **pandas**, **boto3**, **pyarrow**
- **Plotly Dash**
- **macOS Sonoma 13.6.6**

## 🧭 Pipeline Stages

1. Read the raw data directly from S3 (Raw layer).
2. Save initial transformations as the Bronze layer.
3. Clean and enrich the data in the Silver layer.
4. Build business aggregations and metrics in the Gold layer.
5. Display the result in Dash with dynamic filters.

## ✅ Run Locally on macOS

```bash
# Clone the repository
git clone https://github.com/DATAdotPDF/Desafio_Final_DNC_RID211401.git
cd dnc_pipeline

# Create the virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Create a .env file with these variables:
AWS_ACCESS_KEY_ID=your_key
AWS_SECRET_ACCESS_KEY=your_secret
AWS_REGION=sa-east-1
S3_BUCKET_NAME=dncinsight-pipeline-rid211401

# Run the pipeline
bash start.sh

# Run the dashboard
python 06_dashboard/app.py
```

### ☁️ Run with Airflow and Docker
```bash
cd 05_docker

# Initialize the environment
docker-compose up airflow-init
docker-compose up
```

Open [http://localhost:8080](http://localhost:8080).  
**Username:** airflow  
**Password:** airflow  

Run the `dnc_pipeline` DAG manually from the interface.

### 📊 Dashboard
The interactive dashboard displays:
- User count by age group and status.
- Percentage of active users by group.
- Average number of days since registration.
- Dynamic filters by age group and status.

### 📌 Notes
- Developed and tested exclusively on macOS.
- Commands and permissions may differ on Windows or Linux.
- Modular structure prepared for a future cloud deployment or public release.

---

## 📚 References

- [DNC Data School](https://www.escoladnc.com.br)
- [AWS S3](https://aws.amazon.com/pt/s3/)
- [Plotly Dash](https://dash.plotly.com/)
- [Apache Airflow](https://airflow.apache.org/)
- [SIDRA Project GitHub](https://github.com/DATAdotPDF/Desafio_Pratico_DNC_Grupo6)

Developed by [Pedro Ferreira – LinkedIn](https://www.linkedin.com/in/datadotpdf)