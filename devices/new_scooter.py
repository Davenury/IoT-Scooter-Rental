from datetime import datetime

import psycopg2
import sys
sys.path.append("..")
from devices.Scooter import Scooter, get_random_mac, get_random_string


def scooter_from_dict(**kwargs):
    vehicle_type = kwargs.get('vehicle_type', 1)
    mac = kwargs.get('mac', get_random_mac())
    battery_model = kwargs.get('battery_model', get_random_string(6))
    scooter = create_new_scooter_and_get_its_id(vehicle_type, mac, battery_model)

    scooter.last_known_point = (kwargs.get('y', 19.909286), kwargs.get('x', 50.088594))
    scooter.last_telemetry.battery = kwargs.get('battery_level', 100)
    scooter.last_telemetry.point = scooter.last_known_point
    scooter.last_telemetry.time = kwargs.get('time', datetime.timestamp(datetime.now()))
    scooter.last_telemetry.battery_temp = kwargs.get('battery_temp', 30)
    return scooter


class ScooterFactory:
    @staticmethod
    def create(**kwargs):
        scooter = scooter_from_dict(**kwargs)
        if kwargs.get("set_custom_battery_functions", False):
            drop_function = lambda scooter: ScooterFactory.new_scooter_battery_drop_function(scooter)
            raise_function = lambda scooter: ScooterFactory.new_scooter_battery_temp_raise_function(scooter)
            scooter.set_battery_drop_function(drop_function)
            scooter.set_battery_raise_temp_function(raise_function)
        return scooter

    @staticmethod
    def new_scooter_battery_drop_function(scooter):
        return 0.1

    @staticmethod
    def new_scooter_battery_temp_raise_function(scooter):
        return 0.1


def create_new_scooter_and_get_its_id(vehicle_type: int, mac: str,
                                      battery_model: str):
    conn = psycopg2.connect(host="scooter-database.cciikk1f6cy6.us-east-1.rds.amazonaws.com", port=5432,
                            dbname="postgres", user="scooter",
                            password="scooter1"
                            )

    conn.autocommit = True

    cur = conn.cursor()

    cur.execute(
        'insert into scooters(battery_model, mac, vehicle_type) VALUES (%s, %s, %s);',
        (battery_model, mac, vehicle_type)
    )

    cur.execute(
        'select id from scooters where battery_model=%s and mac=%s and vehicle_type = %s',
        (battery_model, mac, vehicle_type)
    )

    id = cur.fetchone()[0]
    scooter = Scooter(id)
    return scooter

