from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta

def extract():
    print("Extracting data...")

def transform():
    print("Transforming data...")

def load():
    print("Loading data...")

with DAG(
    'etl_demo',
    default_args={
        'owner': 'opendemo',
        'retries': 1,
        'retry_delay': timedelta(minutes=5),
    },
    start_date=datetime(2026, 6, 1),
    schedule_interval=timedelta(hours=1),
    catchup=False,
) as dag:
    t1 = PythonOperator(task_id='extract', python_callable=extract)
    t2 = PythonOperator(task_id='transform', python_callable=transform)
    t3 = PythonOperator(task_id='load', python_callable=load)

    t1 >> t2 >> t3
