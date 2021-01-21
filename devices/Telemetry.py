import json
from random import random

from simulation.Simulation import get_basic, get_zone


class Telemetry:
    def __init__(self,
                 scooter_id: int,
                 user_id: int,
                 ride_id: int,
                 battery: int,
                 point,
                 time,
                 battery_temp: float,
                 is_charging: bool,
                 battery_model: str,
                 battery_cycle: int,
                 is_locked: bool,
                 length_of_ride_in_seconds: int,
                 kilometers_distance: float,
                 is_riding: bool,
                 zone_id: int,
                 pricing: float,
                 mac: str,
                 vehicle_type: int,
                 reserved: int,
                 ready_to_ride: bool,
                 ):
        self.scooter_id = scooter_id
        self.client_id = user_id
        self.ride_id = ride_id
        self.battery = battery
        self.point = point
        self.time = time
        self.battery_temp = battery_temp
        self.is_charging = is_charging
        self.battery_model = battery_model
        self.battery_cycle = battery_cycle
        self.is_locked = is_locked
        self.length_of_ride_in_seconds = length_of_ride_in_seconds
        self.kilometers_distance = kilometers_distance
        self.is_riding = is_riding
        self.zone_id = zone_id
        self.pricing = pricing
        self.mac = mac
        self.vehicle_type = vehicle_type
        self.reserved = reserved
        self.ready_to_ride = ready_to_ride

    def get_telemetry(self):
        return json.dumps(self.__dict__)

    @staticmethod
    def get_random_telemetry(scooter, start_time):
        time, points = get_basic(scooter.last_known_point)
        battery = 90
        battery_temp = random.randint(20, 60)
        time_of_ride = 0
        kilometers_distance = 0
        pricing = 0
        telemetry = Telemetry(scooter.id,
                              scooter.user_id,
                              scooter.ride,
                              battery,
                              points[0],
                              start_time.timestamp(),
                              round(battery_temp, 2),
                              False,
                              scooter.battery_model,
                              scooter.battery_cycle,
                              False,
                              time_of_ride,
                              kilometers_distance,
                              True,
                              get_zone(points[0]),
                              pricing,
                              scooter.mac,
                              scooter.vehicle_type,
                              -1,
                              True
                              )
        return telemetry