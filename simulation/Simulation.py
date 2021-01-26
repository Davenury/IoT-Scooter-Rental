import json
import string
from time import sleep

from geopy import distance
import openrouteservice
import random
import datetime

from database.begin_ride import set_begin_attributes
from devices import Telemetry
from others.Exceptions import StopSimulationException

TIME_INTERVAL_FOR_NOT_RIDING = 30


krakow_coordx_center, krakow_coordy_center = 50.088594, 19.909286


def get_zone(coord):
    if krakow_coordx_center - 0.1 < coord[1] < krakow_coordx_center + 0.1 and \
            krakow_coordy_center - 0.1 < coord[0] < krakow_coordy_center + 0.1:
        return 1
    return 2


def get_price(zone, time_step):
    return round(0.5 * zone * time_step.seconds / 60, 2)


def get_client():
    with open('..\\others\\credentials.json') as json_file:
        data = json.load(json_file)

    key = data.get('key')
    return openrouteservice.Client(key=key)


def get_shift():
    vertical, horizontal = 0, 0
    while vertical == 0 and horizontal == 0:
        vertical, horizontal = random.uniform(-0.1, 0.1), random.uniform(-0.1, 0.1)
    return vertical, horizontal


def get_basic(prev_point, next_point=None):
    time = 0
    points = []
    while time == 0:
        try:
            shift = get_shift()
            if next_point is None:
                coords = (prev_point, (prev_point[0] + shift[0], prev_point[1] + shift[1]))
            else:
                coords = (prev_point, next_point)
            routes = get_client().directions(coords, profile='cycling-regular', format="geojson")
            time = routes.get('features')[0].get('properties').get('summary').get('duration')
            points = routes.get('features')[0].get('geometry').get('coordinates')
        except:
            pass
    return time, points


# start_time = czas, w którym wysyłamy
def simulate_ride(start_time, scooter, next_point=None):
    time, points = get_basic(scooter.last_telemetry.point, next_point)
    battery = scooter.last_telemetry.battery
    time_step = datetime.timedelta(
        seconds=time / len(points))
    battery_temp = scooter.last_telemetry.battery_temp
    battery_temp_end = battery_temp + random.randint(5, 19)
    battery_temp_rise_step = (battery_temp_end - battery_temp) / len(points)
    time_of_ride = 0
    kilometers_distance = 0
    prev_point = scooter.last_telemetry.point
    pricing = 0
    for idx, point in enumerate(points):
        start_time += time_step
        battery -= scooter.battery_drop_step(point)
        battery_temp += scooter.battery_raise_temp_step(battery_temp_rise_step)
        time_of_ride += time_step.seconds
        kilometers_distance += distance.distance(point, prev_point).km
        scooter.last_known_point = point
        zone = get_zone(point)
        pricing += get_price(zone, time_step)
        telemetry = Telemetry.Telemetry(scooter.id,
                              scooter.user_id,
                              scooter.ride,
                              battery,
                              point,
                              start_time.timestamp(),
                              round(battery_temp, 2),
                              False,
                              scooter.battery_model,
                              scooter.battery_cycle,
                              False,
                              time_of_ride,
                              kilometers_distance,
                              True,
                              zone,
                              pricing,
                              scooter.mac,
                              scooter.vehicle_type,
                              -1,
                              True,
                              )
        scooter.last_telemetry = telemetry
        if battery <= 5:
            scooter.last_telemetry.battery = 0
        yield telemetry.get_telemetry()
        prev_point = point
        if battery <= 5:
            raise StopSimulationException()


def simulate_stop(scooter):
    scooter.ride = -1
    time_of_not_riding_in_seconds = random.randint(5, 43200)
    ticks_in_not_riding = time_of_not_riding_in_seconds / TIME_INTERVAL_FOR_NOT_RIDING
    is_charging = random.choice([True, False])
    if scooter.last_telemetry.battery < 20:
        is_charging = True
        scooter.last_telemetry.battery = 20
    is_locked = True
    battery_charging_step = 0 if not is_charging else random.randint(round(scooter.last_telemetry.battery, 0), 100) / ticks_in_not_riding
    if not is_charging:
        is_locked = random.choice([True, False])
    scooter.ride = -1
    scooter.last_telemetry.is_charging = is_charging
    scooter.last_telemetry.is_riding = False
    scooter.last_telemetry.locked = is_locked
    scooter.last_telemetry.battery_cycle += 1
    scooter.battery_cycle += 1
    scooter.last_telemetry.length_of_ride_in_seconds = 0
    scooter.last_telemetry.kilometers_distance = 0
    scooter.last_telemetry.is_riding = False
    scooter.last_telemetry.pricing = 0
    scooter.last_telemetry.client_id = -1
    scooter.last_telemetry.ride_id = -1
    if random.randint(0, 10) < 2:
        scooter.last_telemetry.reserved_by = random.randint(0, 6)
    if scooter.last_telemetry.battery < 30:
        scooter.last_telemetry.ready_to_ride = False
    battery_temp_drop_step = max(random.randint(-20, 0), scooter.last_telemetry.battery_temp - 100)\
        if is_charging else random.randint(0, scooter.last_telemetry.battery_temp-20)
    battery_temp_drop_step /= ticks_in_not_riding
    for i in range(0, time_of_not_riding_in_seconds, TIME_INTERVAL_FOR_NOT_RIDING):
        scooter.last_telemetry.battery += battery_charging_step
        scooter.last_telemetry.time += min(TIME_INTERVAL_FOR_NOT_RIDING, time_of_not_riding_in_seconds-i)
        scooter.last_telemetry.battery_temp -= battery_temp_drop_step
        if scooter.last_telemetry.battery > 100:
            scooter.last_telemetry.battery = 100
        yield scooter.last_telemetry.get_telemetry()


def simulate_one_ride(year, month, day, hour, minutes, seconds, scooter, mode="print", next_point=None):
    date = datetime.datetime(year, month, day, hour, minutes, seconds)
    scooter.last_telemetry.time = date.timestamp()
    if mode == "send":
        scooter.send_begin(scooter.last_telemetry.get_telemetry())
        set_begin_attributes(scooter)
    try:
        if mode == "send":
            while scooter.user_id == -1:
                pass
        for item in simulate_ride(datetime.datetime.fromtimestamp(scooter.last_telemetry.time), scooter, next_point):
            if mode == "send":
                scooter.send(item)
            elif mode == "print":
                print(item)
        if mode == "send":
            scooter.send_end(scooter.last_telemetry.get_telemetry())

    except StopSimulationException:
        if mode == "send":
            scooter.send_end(scooter.last_telemetry)
        if mode == "print":
            print("Too low battery for continue riding!")
        scooter.last_telemetry.battery = 90
        scooter.last_telemetry.time += 10600


def simulate(year, month, day, hour, minutes, seconds, scooter, simulation_times=random.randint(5, 10), mode="send"):
    date = datetime.datetime(year, month, day, hour, minutes, seconds)
    scooter.last_telemetry.time = date.timestamp()
    for i in range(0, simulation_times):
        simulate_one_ride(year, month, day, hour, minutes, seconds, scooter, mode)
        for item in simulate_stop(scooter):
            if mode == "send":
                scooter.send(item)
            elif mode == "print":
                print(item)
