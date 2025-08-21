from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.bash import BashOperator

default_args = {
    "owner": "airflow",
    "depends_on_past": False,
    "retries": 1,
    "retry_delay": timedelta(minutes=5),
}

with DAG(
    dag_id="fraud_detection_daily",
    default_args=default_args,
    start_date=datetime(2025, 8, 1),
    schedule_interval="@daily",
    catchup=False,
    description="Daily ETL + model scoring for fraud detection",
) as dag:

    etl = BashOperator(
        task_id="etl_build_features",
        bash_command="python scripts/etl_pipeline.py --run_all"
    )

    train = BashOperator(
        task_id="train_eval",
        bash_command="python scripts/model_train.py --train --eval"
    )

    anomalies = BashOperator(
        task_id="unsupervised_anomaly",
        bash_command="python scripts/anomaly_detection.py --score"
    )

    etl >> [train, anomalies]
