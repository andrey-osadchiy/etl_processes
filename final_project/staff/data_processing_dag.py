from airflow import DAG
from airflow.providers.yandex.operators.yandexcloud_dataproc import DataprocCreatePysparkJobOperator
from datetime import datetime

YC_DP_CLUSTER_ID = 'c9quhbgni0nl9loms74k'
YC_BUCKET = 'examen'

with DAG(
    'family_data_processing_v3',
    schedule_interval='@daily',
    start_date=datetime(2025, 6, 1),
    catchup=False,
    tags=['data-processing']
) as dag:

    process_data = DataprocCreatePysparkJobOperator(
        task_id='process_data',
        cluster_id=YC_DP_CLUSTER_ID,
        main_python_file_uri=f's3a://{YC_BUCKET}/scripts/process_data.py',
        args=[
            '--input', f's3a://{YC_BUCKET}/file/family.csv',
            '--output', f's3a://{YC_BUCKET}/results/{datetime.now().strftime("%Y%m%d_%H%M%S")}'
        ],
        properties={
            'spark.sql.legacy.timeParserPolicy': 'LEGACY',  # Для совместимости формата даты
            'spark.driver.memory': '2g'
        }
    )