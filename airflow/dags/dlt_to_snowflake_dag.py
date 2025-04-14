from airflow import DAG
from airflow.operators.bash import BashOperator
from datetime import datetime

default_args = {
    'owner': 'brentford',
    'start_date': datetime(2024, 1, 1),
    'retries': 1,
}

with DAG(
    dag_id='dlt_to_snowflake_dag',
    default_args=default_args,
    schedule_interval='@daily',
    catchup=False,
    tags=['brentford', 'bronze', 'dlt'],
) as dag:

    run_dlt_pipeline = BashOperator(
        task_id='run_dlt_pipeline',
        bash_command='cd /opt/airflow/etl_pipeline && python etl_pipeline.py',
    )

    run_dlt_pipeline
