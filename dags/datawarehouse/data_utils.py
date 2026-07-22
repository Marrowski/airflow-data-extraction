from airflow.providers.postgres.hooks.postgres import PostgresHook
from psycopg2.extras import RealDictCursor

table = "airflow"

def establish_conn():
    hook = PostgresHook(postgres_conn_id="airflow_db")
    conn = hook.get_conn()
    cursor = conn.cursor(cursor_factory=RealDictCursor)

    return conn, cursor


def close_conn(conn, cursor):
    cursor.close()
    conn.close()


def create_schema(schema):
    conn, cur = establish_conn()

    schema_sql = f"CREATE SCHEMA IF NOT EXISTS {schema}"

    cur.execute(schema_sql)
    conn.commit()

    close_conn(conn, cur)


def create_table(schema):
    conn, cur = establish_conn()

    if schema == "staging":
        sql_table = f'''
        CREATE TABLE IF NOT EXISTS {schema}.{table} (
        "Video_ID" VARCHAR(11) PRIMARY KEY NOT NULL,
        "Video_Title" TEXT NOT NULL,
        "Upload_Date" TIMESTAMP NOT NULL,
        "Duration" VARCHAR(20) NOT NULL,
        "Video_Views" INT,
        "Likes_Count" INT,
        "Comments_Count" INT  
        );     
    '''
    else:
        sql_table = f'''
                CREATE TABLE IF NOT EXISTS {schema}.{table} (
                "Video_ID" VARCHAR(11) PRIMARY KEY NOT NULL,
                "Video_Title" TEXT NOT NULL,
                "Upload_Date" TIME NOT NULL,
                "Duration" VARCHAR(20) NOT NULL,
                "Video_Type" VARCHAR(10) NOT NULL,
                "Video_Views" INT,
                "Likes_Count" INT,
                "Comments_Count" INT  
                );     
            '''
    cur.execute(sql_table)
    conn.commit()
    close_conn(conn, cur)


def get_video_ids(cur, schema):
    cur.execute(f"""SELECT "Video_ID" FROM {schema}.{table}""")
    ids = cur.fetchall()

    video_ids = [row['Video_ID'] for row in ids]
    return video_ids