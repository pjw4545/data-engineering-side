from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta

# news_crawler.py 파일에서 main 함수를 임포트합니다.
# Airflow worker가 이 파일을 찾을 수 있도록 PYTHONPATH에 dags 폴더가 포함되거나,
# news_crawler.py가 dags 폴더 내에 있어야 합니다.
# 여기서는 news_crawler.py가 dags 폴더 내에 있다고 가정합니다.
from news_crawler import main as run_news_crawler_script

with DAG(
    dag_id='news_collection_10min',
    start_date=datetime(2023, 1, 1),
    schedule_interval=timedelta(minutes=10), # 10분마다 실행
    catchup=False,
    tags=['data_collection', 'news', 'frequent'],
    default_args={
        'owner': 'airflow',
        'depends_on_past': False,
        'email_on_failure': False,
        'email_on_retry': False,
        'retries': 1,
        'retry_delay': timedelta(minutes=5),
    },
) as dag:
    collect_news_task = PythonOperator(
        task_id='collect_news_data_every_10_min',
        python_callable=run_news_crawler_script,
    )