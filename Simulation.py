import json
from time import sleep
from geopy import distance
import string
import openrouteservice
import random
import datetime
from typing import List

from Scooter import Scooter

TIME_INTERVAL_FOR_NOT_RIDING = 30


def get_random_string(length):
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(length))


scooters = [Scooter(get_random_string(10)) for i in range(10)]

krakow_coordx_center, krakow_coordy_center = 50.088594, 19.909286


def get_zone(coord):
    if krakow_coordx_center - 0.1 < coord[1] < krakow_coordx_center + 0.1 and \
            krakow_coordy_center - 0.1 < coord[0] < krakow_coordy_center + 0.1:
        return 1
    return 2


def get_price(zone, time_step):
    return round(0.5 * zone * time_step.seconds / 60, 2)


class Telemetry:
    def __init__(self,
                 user_id: int,
                 ride_id: int,
                 battery: int,
                 point,
                 time,
                 battery_temp: float,
                 is_charging: bool,
                 battery_model: str,
                 battery_circle: int,
                 locked: bool,
                 length_of_ride_in_seconds: int,
                 kilometers_distance: int,
                 is_riding: bool,
                 zone_id: int,
                 pricing: float,
                 mac: string,
                 vehicle_type: int,
                 reserved: dict,
                 ready_to_ride: bool
                 ):
        self.user_id = user_id
        self.ride_id = ride_id
        self.battery = battery
        self.point = point
        self.time = time
        self.battery_temp = battery_temp
        self.is_charging = is_charging
        self.battery_model = battery_model
        self.battery_circle = battery_circle
        self.locked = locked
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


def get_client():
    with open('credentials.json') as json_file:
        data = json.load(json_file)

    key = data.get('key')
    return openrouteservice.Client(key=key)


def get_shift():
    vertical, horizontal = random.uniform(0, 0.1), random.uniform(0, 0.1)
    return vertical, horizontal


# coords = ((19.914522, 50.070803), (19.909029, 50.088318))


def get_basic(prev_point):
    shift = get_shift()
    coords = (prev_point, (prev_point[0] + shift[0], prev_point[1] + shift[1]))
    routes = get_client().directions(coords, profile='cycling-regular', format="geojson")
    time = routes.get('features')[0].get('properties').get('summary').get('duration')
    points = routes.get('features')[0].get('geometry').get('coordinates')
    battery = random.randint(20, 100)
    return time, points, battery


# start_time = czas, w którym wysyłamy
def simulate_ride(start_time, scooter):
    time, points, battery = get_basic(scooter.last_known_point)
    battery_drop_step, time_step = random.randrange(10, battery) / len(points), datetime.timedelta(
        seconds=time / len(points))
    battery_temp = random.randint(20, 60)
    battery_temp_end = battery_temp + random.randint(5, 19)
    battery_temp_rise_step = (battery_temp_end - battery_temp) / len(points)
    time_of_ride = 0
    kilometers_distance = 0
    prev_point = points[0]
    for point in points:
        start_time += time_step
        battery -= battery_drop_step
        battery_temp += battery_temp_rise_step
        time_of_ride += time_step.seconds
        kilometers_distance += distance.distance(point, prev_point).km
        scooter.last_known_point = point
        zone = get_zone(point)
        pricing = get_price(zone, time_step)
        telemetry = Telemetry(scooter.user_id,
                              scooter.ride,
                              battery,
                              point,
                              start_time.timestamp(),
                              round(battery_temp, 2),
                              False,
                              scooter.battery_model,
                              scooter.battery_circle,
                              False,
                              time_of_ride,
                              kilometers_distance,
                              True,
                              zone,
                              pricing,
                              scooter.mac,
                              scooter.vehicle_type,
                              {
                                  "is_reserved": False,
                                  "reserved_by": None
                              },
                              True
                              )
        scooter.last_telemetry = telemetry
        yield telemetry.get_telemetry()
        prev_point = point
    scooter.iterate_ride()


def simulate_stop(scooter):
    time_of_not_riding_in_seconds = random.randint(5, 43200)
    ticks_in_not_riding = time_of_not_riding_in_seconds / TIME_INTERVAL_FOR_NOT_RIDING
    is_charging = random.choice([True, False])
    is_locked = True
    battery_charging_step = 0 if not is_charging else random.randint(round(scooter.last_telemetry.battery, 0), 100) / ticks_in_not_riding
    if not is_charging:
        is_locked = random.choice([True, False])
    scooter.last_telemetry.is_charging = is_charging
    scooter.last_telemetry.is_riding = False
    scooter.last_telemetry.locked = is_locked
    scooter.last_telemetry.battery_circle += 1
    scooter.battery_circle += 1
    scooter.last_telemetry.length_of_ride_in_seconds = 0
    scooter.last_telemetry.kilometers_distance = 0
    scooter.last_telemetry.is_riding = False
    scooter.last_telemetry.pricing = 0
    scooter.last_telemetry.user_id = -1
    if random.randint(0, 10) < 2:
        scooter.last_telemetry.reserved.is_reserved = True
        scooter.last_telemetry.reserved.reserved_by = "player_1"
    if scooter.last_telemetry.battery < 30:
        scooter.last_telemetry.ready_to_ride = False
    battery_temp_drop_step = max(random.randint(-20, 0), scooter.last_telemetry.battery_temp - 100)\
        if is_charging else random.randint(0, scooter.last_telemetry.battery_temp-20)
    battery_temp_drop_step /= ticks_in_not_riding
    for i in range(0, time_of_not_riding_in_seconds, TIME_INTERVAL_FOR_NOT_RIDING):
        scooter.last_telemetry.battery += battery_charging_step
        scooter.last_telemetry.time += min(TIME_INTERVAL_FOR_NOT_RIDING, time_of_not_riding_in_seconds-i)
        scooter.last_telemetry.battery_temp -= battery_temp_drop_step
        yield scooter.last_telemetry.get_telemetry()


def simulate(year, month, day, hour, minutes, seconds, scooter):
    date = datetime.datetime(year, month, day, hour, minutes, seconds)
    items = []
    for item in simulate_ride(date, scooter):
        items.append(item)
        #scooter.send(item)
        #sleep(0.01)
        #scooter.receive()
    for item in simulate_stop(scooter):
        items.append(item)
        #scooter.send(item)
        #sleep(0.01)
        #scooter.receive()
    with open('results.txt', "w+") as file:
        json.dump(items, file)


simulate(2010, 3, 10, 18, 25, 19, scooters[0])
