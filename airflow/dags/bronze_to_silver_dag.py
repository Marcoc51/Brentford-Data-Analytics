from airflow import DAG
from airflow.operators.bash import BashOperator
from datetime import datetime

default_args = {
    'owner': 'brentford',
    'start_date': datetime(2024, 1, 1),
    'retries': 1,
}

with DAG(
    dag_id='bronze_to_silver_dag',
    default_args=default_args,
    schedule_interval='@daily',
    catchup=False,
    tags=['brentford', 'silver', 'dbt'],
) as dag:

    run_dbt = BashOperator(
        task_id='run_dbt_models',
        bash_command='cd /opt/airflow/snowflake_dbt && dbt run',
    )

    run_dbt
