import sys
import os
import json
import psycopg2


def handler(event, contex):
    try:
        conn = psycopg2.connect(host=os.environ['rds_host'], port=os.environ['rds_port'],
                                dbname=os.environ['rds_dbname'], user=os.environ['rds_username'],
                                password=os.environ['rds_password']
                                )

        conn.autocommit = True

        cur = conn.cursor()

        cur.execute(
            'update rides set kilometers_distance=%s, pricing=%s, end_time=to_timestamp(%s) where id=%s',
            (event['kilometers_distance'], event['pricing'], event['time'], event['ride_id'])
        )
        conn.commit()

    finally:
        try:
            conn.close()
        except:
            pass
