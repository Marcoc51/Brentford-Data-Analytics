from airflow import DAG
from airflow.operators.bash import BashOperator
from datetime import datetime

default_args = {
    'owner': 'brentford',
    'start_date': datetime(2024, 1, 1),
    'retries': 1,
}

with DAG(
    dag_id='scrape_to_postgres_dag',
    default_args=default_args,
    schedule_interval='@daily',
    catchup=False,
    tags=['brentford', 'bronze'],
) as dag:

    scrape_and_load = BashOperator(
        task_id='scrape_and_load',
        bash_command='python /opt/airflow/scripts/scraper.py',
    )

    scrape_and_load
