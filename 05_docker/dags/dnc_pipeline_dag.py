from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime
from etl_pipeline import run_etl

default_args = {
    "owner": "airflow",
    "start_date": datetime(2024, 1, 1),
    "retries": 1,
}

with DAG(
    dag_id='dnc_pipeline',
    start_date=datetime(2025, 7, 25),
    schedule_interval=None,
    catchup=False,
    default_args=default_args,
    tags=['etl', 'dnc']
) as dag:
    
    executar_pipeline_etl = PythonOperator(
        task_id='executar_pipeline_etl',
        python_callable=run_etl
    )

    executar_pipeline_etl
