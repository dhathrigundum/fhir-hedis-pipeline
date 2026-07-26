"""Placeholder orchestration skeleton for the HEDIS ELT pipeline.

No-op tasks in the intended real order. Section 10.3 replaces each task
with the real command once the warehouse connection exists:
  load  -> ingestion/parse_bundles.py + GCS/BigQuery load
  dbt run  -> staging -> intermediate -> marts
  dbt test -> data tests on the marts layer
  refresh  -> mart is ready for the dashboard to query
"""

from datetime import datetime

from airflow import DAG
from airflow.operators.empty import EmptyOperator

with DAG(
    dag_id="hedis_pipeline",
    description="Load Synthea FHIR data, transform with dbt, refresh CBP marts",
    schedule=None,
    start_date=datetime(2026, 1, 1),
    catchup=False,
    tags=["hedis", "cbp", "placeholder"],
) as dag:
    load = EmptyOperator(task_id="load_raw_data")
    dbt_run = EmptyOperator(task_id="dbt_run")
    dbt_test = EmptyOperator(task_id="dbt_test")
    refresh = EmptyOperator(task_id="refresh_marts")

    load >> dbt_run >> dbt_test >> refresh