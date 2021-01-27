from datetime import datetime
from time import sleep

import psycopg2
import sys
sys.path.append("..")
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
            "select * from scooters as s left join scooter_info as si on s.id = si.scooter_id where s.id = %s"
            " order by actual_time desc limit 1",
            (scooter_id,)
        )
        info = cur.fetchone()

        cur.execute(
            "select ST_X(location), ST_Y(location) from scooters as s left join scooter_info as si on s.id = si.scooter_id where s.id = %s"
            "order by actual_time desc limit 1",
            (scooter_id,)
        )
        x, y = cur.fetchone()
        return info, x, y


    finally:
        try:
            conn.close()
        except:
            pass


def prepare_scooter(scooter):
    info, x, y = get_info(scooter.id)
    scooter.battery_model = info[1]
    scooter.mac = info[2]
    scooter.vehicle_type = info[3]
    if info[5] is not None:
        scooter.last_telemetry = Telemetry.Telemetry(
            scooter.id,
            -1,
            -1,
            info[8],
            (x, y),
            datetime.timestamp(info[5]),
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
    else:
        scooter.last_telemetry = Telemetry.Telemetry.get_random_telemetry(scooter)


if __name__ == "__main__":
    scooter = Scooter.Scooter(1)
    print(scooter.last_telemetry.get_telemetry())
