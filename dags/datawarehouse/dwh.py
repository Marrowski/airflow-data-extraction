from .data_utils import establish_conn, close_conn, create_schema, create_table, get_video_ids
from .data_loading import load_path
from .data_modification import insert_rows, update_rows, delete_rows
from .data_transformation import transform_data


import logging
from airflow.decorators import task

logger = logging.getLogger(__name__)
table = "airflow"

@task
def staging_table():

    schema = 'staging'

    conn,cur = None, None

    try:
        conn, cur = establish_conn()
        YT_data = load_path()

        create_schema(schema)
        create_table(schema)

        table_ids = get_video_ids(cur, schema)

        for row in YT_data:
            if len(table_ids) == 0:
                insert_rows(cur, conn, schema, row)
            else:
                if row['video_id'] in table_ids:
                    update_rows(cur, conn, schema, row)
                else:
                    insert_rows(cur, conn, schema, row)

        ids_in_json = {row['video_id'] for row in YT_data}
        ids_to_delete = set(table_ids) - ids_in_json

        if ids_to_delete:
            delete_rows(cur, conn, schema, ids_to_delete)

        logger.info(f"{schema} table update completed")

    except Exception as e:
        logger.error(f"An error occurred during the update of {schema} table: {e}")
        raise

    finally:
        if conn and cur:
            close_conn(conn, cur)

@task
def core_table():
    schema = "core"
    conn, cur = None, None

    try:
        conn, cur = establish_conn()
        create_schema(schema)
        create_table(schema)

        table_ids = get_video_ids(cur, schema)

        current_video_ids = set()

        cur.execute(f"SELECT * FROM staging.{table};")
        rows = cur.fetchall()

        for row in rows:
            current_video_ids.add(row["Video_ID"])

            if len(table_ids) == 0:
                transformed_row = transform_data(row)
                insert_rows(cur, conn, schema, transformed_row)
            else:
                transformed_row = transform_data(row)

                if transformed_row['Video_ID'] in table_ids:
                    update_rows(cur, conn, schema, transformed_row)

                else:
                    insert_rows(cur, conn, schema, transformed_row)

        ids_to_delete = set(table_ids) - current_video_ids

        if ids_to_delete:
            delete_rows(conn, cur, schema, ids_to_delete)

        logger.info(f"{schema} table update completed")

    except Exception as e:
        logger.error(f"An error occurred while updating {schema} table:{e}")
        raise e

    finally:
        if conn and cur:
            close_conn(conn, cur)