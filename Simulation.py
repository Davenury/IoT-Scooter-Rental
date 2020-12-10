import json
from time import sleep

import openrouteservice
import random
import datetime


class Telemetry:
    def __init__(self, battery: int, point, time):
        self.battery = battery
        self.point = point
        self.time = time

    def get_telemetry(self):
        return json.dumps(self.__dict__)


def get_client():
    with open('credentials.json') as json_file:
        data = json.load(json_file)

    key = data.get('key')
    return openrouteservice.Client(key=key)


vertical, horizontal = random.uniform(0, 1), random.uniform(0, 1)
coordx, coordy = 50.088594, 19.909286

coords = ((19.914522, 50.070803), (19.909029, 50.088318))


def get_basic():
    routes = get_client().directions(coords, profile='cycling-regular', format="geojson")
    time = routes.get('features')[0].get('properties').get('summary').get('duration')
    points = routes.get('features')[0].get('geometry').get('coordinates')
    battery = random.randint(20, 100)
    return time, points, battery


def simulate(start_time):
    time, points, battery = get_basic()
    battery_step, time_step = random.randrange(10, battery) / len(points), datetime.timedelta(seconds=time/len(points))
    for point in points:
        start_time += time_step
        battery -= battery_step
        yield Telemetry(battery, point, start_time.timestamp()).get_telemetry()


def try_out(year, month, day, hour, minutes, seconds):
    for item in simulate(datetime.datetime(year, month, day, hour, minutes, seconds)):
        print(item)
        sleep(0.1)


try_out(2010, 3, 10, 18, 25, 19)
