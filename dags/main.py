from airflow import DAG
import pendulum
from datetime import datetime, timedelta
from api.extract_video_data import get_playlist_id, get_video_ids, extract_video_data, save_to_json
from dataquality.soda import check_data_quality

from datawarehouse.dwh import staging_table, core_table

from airflow.operators.trigger_dagrun import TriggerDagRunOperator

local_tz = pendulum.timezone("Europe/Kyiv")

default_args = {
    "owner": "Marrowski",
    "depends_on_past": False,
    "email_on_failure": False,
    "email_on_retry": False,
    "email": "emelianov2811@gmail.com",
    # "retries": 1,
    # "retry_delay": timedelta(hours=1),
    "max_active_runs": 1,
    "dagrun_timeout": timedelta(hours=1),
    "start_date": datetime(2026, 7,21, tzinfo=local_tz),
    # "end_date": datetime(2030, 7,21, tzinfo=local_tz)
}

staging_schema = "staging"
core_schema = "core"

with DAG(
    dag_id='produce_json',
    default_args=default_args,
    description="DAG to produce json file with youtube data",
    schedule="0 14 * * *",
    catchup=False
) as dag_produce:

    playlist_id = get_playlist_id()
    video_ids = get_video_ids(playlist_id)
    extract_data = extract_video_data(video_ids)
    save = save_to_json(extract_data)

    trigger_update_db = TriggerDagRunOperator(
        task_id="trigger_update_db",
        trigger_dag_id="update_db",
    )


    playlist_id >> video_ids >> extract_data >> save >> trigger_update_db


with DAG(
    dag_id='update_db',
    default_args=default_args,
    description="DAG to proccess JSON file and insort date into staging and core schemas",
    schedule=None,
    catchup=False
) as dag_update:

    update_staging = staging_table()
    update_core = core_table()

    trigger_data_quality = TriggerDagRunOperator(
        task_id="trigger_data_check",
        trigger_dag_id="data_check",
    )

    update_staging >> update_core >> trigger_data_quality

with DAG(
    dag_id='data_check',
    default_args=default_args,
    description="DAG to execute data quality checks",
    schedule=None,
    catchup=False
) as dag_quality:

    data_quality_test_staging = check_data_quality(staging_schema)
    data_quality_test_core = check_data_quality(core_schema)

    data_quality_test_staging >> data_quality_test_core