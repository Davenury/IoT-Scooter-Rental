from time import sleep

import psycopg2

from devices import Scooter
from devices import Telemetry


def get_info(scooter_id):
    try:
        conn = psycopg2.connect(host="scooter-database.cciikk1f6cy6.us-east-1.rds.amazonaws.com", port=5432,
                                dbname="postgres", user="scooter",
                                password="scooter1"
                                )

        conn.autocommit = True

        cur = conn.cursor()

        cur.execute(
            "select * from scooters as s join scooter_info as si on s.id = si.scooter_id where s.id = %s"
            " order by actual_time desc limit 1",
            (scooter_id,)
        )
        info = cur.fetchone()
        return info


    finally:
        try:
            conn.close()
        except:
            pass


def prepare_scooter(scooter):
    info = get_info(scooter.id)
    scooter.battery_model = info[1]
    scooter.mac = info[2]
    scooter.vehicle_type = info[3]
    scooter.last_telemetry = Telemetry.Telemetry(
        scooter.id,
        -1,
        -1,
        info[8],
        info[7],
        info[5],
        info[9],
        info[11],
        scooter.battery_model,
        info[10],
        info[12],
        0,
        0,
        info[13],
        info[16],
        0,
        scooter.mac,
        scooter.vehicle_type,
        info[14],
        info[15]
    )
