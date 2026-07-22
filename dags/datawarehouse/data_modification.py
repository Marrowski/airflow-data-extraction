import logging


logger = logging.getLogger(__name__)
table = "airflow"

def insert_rows(cur, conn, schema, row):

    try:
        if schema == "staging":
            video_id = "video_id"

            cur.execute(
                f"""INSERT INTO {schema}.{table}("Video_ID", "Video_Title", "Upload_Date", "Duration", "Video_Views", "Likes_Count", "Comments_Count")
                VALUES (%(video_id)s, %(title)s, %(published_at)s, %(duration)s, %(viewCount)s, %(likeCount)s, %(commentCount)s);
                """, row
            )
        else:
            video_id = 'Video_ID'

            cur.execute(
                f"""INSERT INTO {schema}.{table}("Video_ID", "Video_Title", "Upload_Date", "Duration", "Video_Type", "Video_Views", "Likes_Count", "Comments_Count")
                    VALUES (%(Video_ID)s, %(Video_Title)s, %(Upload_Date)s, %(Duration)s, %(Video_Type)s, %(Video_Views)s, %(Likes_Count)s, %(Comments_Count)s);
                    """, row
            )

        conn.commit()

        vid = row.get('video_id') or row.get('Video_ID')
        logger.info(f"Inserted row with Video_ID: {vid}")

    except Exception as e:
        vid = row.get('video_id') or row.get('Video_ID')
        logger.error(f"Error inserting row with Video_ID: {vid} - {e}")
        raise e


def update_rows(cur, conn, schema, row):
    try:
        if schema == "staging":
            cur.execute(
                f"""
                UPDATE {schema}.{table}
                SET "Video_Title" = %(title)s,
                    "Video_Views" = %(viewCount)s,
                    "Likes_Count" = %(likeCount)s,
                    "Comments_Count" = %(commentCount)s
                WHERE "Video_ID" = %(video_id)s;
                """, row
            )
            video_id = row['video_id']
        else:
            cur.execute(
                f"""
                UPDATE {schema}.{table}
                SET "Video_Title" = %(Video_Title)s,
                    "Video_Views" = %(Video_Views)s,
                    "Likes_Count" = %(Likes_Count)s,
                    "Comments_Count" = %(Comments_Count)s
                WHERE "Video_ID" = %(Video_ID)s;
                """, row
            )
            video_id = row['Video_ID']

        conn.commit()

        logger.info(f"Updated row with Video_ID: {video_id}")

    except Exception as e:
        logger.error(f"Error updating row: {e}")
        raise e


def delete_rows(cur, conn, schema, ids):

    try:
        ids = f"""({', '.join(f"{id}" for id in ids)})"""

        cur.execute(
            f"""
            DELETE FROM {schema}.{table}
            WHERE "Video_ID" IN {ids}
            """
        )

        conn.commit()

        logger.info(f"Deleted row with Video_ID: {ids}")

    except Exception as e:
        logger.error(f"Error deleting row with Video_ID: {ids} - {e}")
        raise e