import sys
import os
import json
import psycopg2
import boto3


def handler(event, contex):
    try:
        if event['client_id'] == -1:
            conn = psycopg2.connect(host=os.environ['rds_host'], port=os.environ['rds_port'],
                                    dbname=os.environ['rds_dbname'], user=os.environ['rds_username'],
                                    password=os.environ['rds_password']
                                    )

            conn.autocommit = True

            cur = conn.cursor()

            cur.execute(
                'select id from clients order by random() limit 1'
            )
            client_id = cur.fetchone()[0]
            print(client_id)

            point = 'POINT({0} {1})'.format(event['point'][0], event['point'][1])
            cur.execute(
                'insert into scooter_info (actual_time, scooter_id, location, battery_level, battery_temp, battery_cycle, is_charging, is_locked, is_riding, reserved_by, ready_to_ride, zone_id) VALUES (to_timestamp(%s), %s, ST_GeomFromText(%s), %s, %s, %s, %s, %s, %s, %s, %s, %s)',
                (event['time'], event['scooter_id'], point, event['battery'], event['battery_temp'],
                 event['battery_cycle'], event['is_charging'], event['is_locked'],
                 event['is_riding'], event['reserved'], event['ready_to_ride'], event['zone_id'])
            )
            cur.execute(
                'select actual_time from scooter_info where scooter_id = %s order by actual_time desc limit 1',
                (event['scooter_id'],)
            )
            start_time = cur.fetchone()[0]

            cur.execute(
                'insert into rides(client_id, scooter_id, start_time, end_time, kilometers_distance, pricing) values (%s, %s, %s, %s, %s, %s)',
                (client_id, event['scooter_id'], start_time, start_time, 0, 0)
            )

            cur.execute(
                'select id from rides where scooter_id = %s and client_id = %s and start_time = %s',
                (event['scooter_id'], client_id, start_time)
            )
            ride_id = cur.fetchone()[0]
            print(ride_id)

            # client = boto3.client('iot-data')
            # print("here")
            # response = client.publish(
            #        topic="scooter/{0}/begin_response".format(event['scooter_id']),
            #        qos=1,
            #        payload=json.dumps({
            #            'client_id': client_id,
            #            'ride_id': ride_id
            #        })
            #    )
            # print("here2")

    finally:
        try:
            conn.close()
        except:
            pass
