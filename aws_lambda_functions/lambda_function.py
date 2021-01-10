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

        if event['ride_id'] != -1:
            cur.execute(
                'insert into rides_info (point, actual_time, battery_temp, ride_id, length_of_ride_in_seconds, kilometers_distance, zone_id, pricing) values (%s, %s, %s, %s, %s, %s, %s, %s)',
                event['point'], event['time'], event['battery_temp'], event['ride_id'],
                event['length_of_ride_in_seconds'], event['kilometers_distance'], event['zone_id'], event['pricing']
            )

            cur.execute(
                'update rides set end_time=%s', (event['time'],)
            )

        cur.execute(
            'update scooter_info set location = %s, battery_level = %s, battery_cycle = %s, is_charging = %s, is_locked = %s, is_riding = %s, reserved_by = %s, ready_to_ride_bool = %s',
            (event['point'], event['battery'], event['battery_cycle'], event['is_charging'], event['is_locked'],
             event['is_riding'], event['reserved'])
            )
    finally:
        try:
            conn.close()
        except:
            pass
