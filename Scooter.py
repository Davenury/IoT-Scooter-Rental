import random

import zmq
import rstr
import string

SCOOTER = "scooter"


def get_random_string(length):
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(length))


def get_random_mac():
    return rstr.xeger(r'[0-9A-F]{2}:[0-9A-F]{2}:[0-9A-F]{2}:[0-9A-F]{2}:[0-9A-F]{2}:[0-9A-F]{2}')


class Scooter:
    def __init__(self, id):
        self.init_zmq()
        self.id = id
        self.battery_model = get_random_string(6)  # -> random battery model
        self.battery_circle = 0
        self.last_known_point = (19.909286, 50.088594)
        self.last_telemetry = None
        self.mac = get_random_mac()
        self.ride = 0
        self.vehicle_type = 1
        self.user_id = 0

    def iterate_ride(self):
        self.ride += 1

    def init_zmq(self):
        self.context = zmq.Context()
        self.socket = self.context.socket(zmq.REQ)
        self.socket.connect("tcp://localhost:5555")

    def send(self, message):
        self.socket.send_json(message)

    def receive(self):
        message = self.socket.recv()
        print(message)

    def set_user_id(self, user_id):
        self.user_id = user_id
