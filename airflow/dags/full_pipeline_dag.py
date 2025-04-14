from airflow import DAG
from airflow.operators.bash import BashOperator
from datetime import datetime

default_args = {
    'owner': 'brentford',
    'start_date': datetime(2024, 1, 1),
    'retries': 1,
}

with DAG(
    dag_id='full_pipeline_dag',
    default_args=default_args,
    schedule_interval='@daily',
    catchup=False,
    tags=['brentford', 'full', 'etl'],
) as dag:

    # 1. Scrape & Load to PostgreSQL
    scrape_to_postgres = BashOperator(
        task_id='scrape_to_postgres',
        bash_command='cd /opt/airflow/scripts && python scraper.py',
    )

    # 2. Run dlt to load PostgreSQL → Snowflake (Bronze)
    dlt_to_snowflake = BashOperator(
        task_id='dlt_to_snowflake',
        bash_command='cd /opt/airflow/etl_pipeline && python etl_pipeline.py',
    )

    # 3. Run dbt to transform Bronze → Silver
    dbt_run = BashOperator(
        task_id='dbt_run_transformations',
        bash_command='cd /opt/airflow/snowflake_dbt && dbt run',
    )

    # Define DAG dependency order
    scrape_to_postgres >> dlt_to_snowflake >> dbt_run
