import sys
import os
import json
import psycopg2
import boto3


def handler(event, contex):
    try:
        conn = psycopg2.connect(host=os.environ['rds_host'], port=os.environ['rds_port'],
                                dbname=os.environ['rds_dbname'], user=os.environ['rds_username'],
                                password=os.environ['rds_password']
                                )

        conn.autocommit = True

        cur = conn.cursor()

        cur.execute(
            'select id from clients order by random()'
        )
        client_id = cur.fetchone()[0]
        print(client_id)

        point = 'POINT({0} {1})'.format(event['point'][0], event['point'][1])
        cur.execute(
            'insert into scooter_info (actual_time, scooter_id, location, battery_level, battery_temp, battery_cycle, is_charging, is_locked, is_riding, reserved_by, ready_to_ride, zone_id) VALUES (to_timestamp(%s), %s, ST_GeomFromText(%s), %s, %s, %s, %s, %s, %s, %s, %s, %s)',
            (event['time'], event['scooter_id'], point, event['battery'], event['battery_temp'], event['battery_cycle'],
             event['is_charging'], event['is_locked'],
             event['is_riding'], event['reserved'], event['ready_to_ride'], event['zone_id'])
        )

        if event['is_riding']:
            cur.execute(
                'update rides set kilometers_distance=%s, pricing=%s, end_time=to_timestamp(%s) where id=%s',
                (event['kilometers_distance'], event['pricing'], event['time'], event['ride_id'])
            )

        state = None
        if event['is_riding']:
            state = 'IN_RUN'
        elif event['is_charging'] or event['reserved_by'] != -1:
            state = 'DISABLED'
        else:
            state = 'AVAILABLE'

        cur.execute(
            'UPDATE scooters set state = %s where id = %s',
            (state, event['scooter_id'])
        )


    finally:
        try:
            conn.close()
        except:
            pass
