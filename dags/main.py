from airflow import DAG
import pendulum
from datetime import datetime, timedelta
from api.extract_video_data import get_playlist_id, get_video_ids, extract_video_data, save_to_json

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

with DAG(
    dag_id='produce_json',
    default_args=default_args,
    description="DAG to produce json file with youtube data",
    schedule="0 14 * * *",
    catchup=False
) as dag:

    playlist_id = get_playlist_id()
    video_ids = get_video_ids(playlist_id)
    extract_data = extract_video_data(video_ids)
    save = save_to_json(extract_data)


    playlist_id >> video_ids >> extract_data >> save
