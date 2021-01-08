import random

import rstr
import string
import os
import paho.mqtt.client as mqtt
import time as t
import json
import AWSIoTPythonSDK.MQTTLib as AWSIoTPyMQTT

dir_path = os.path.dirname(os.path.realpath(__file__))
ENDPOINT = "a1r8jjr1mg7i8s-ats.iot.us-east-1.amazonaws.com"
# CLIENT_ID = "testDevice"
PATH_TO_CERT = "certificates/25ebfe00c3-certificate.pem.crt"
PATH_TO_KEY = "certificates/25ebfe00c3-private.pem.key"
PATH_TO_ROOT = "certificates/CA.pem"
MESSAGE = "Hello World"
TOPIC = "test/testing"
RANGE = 20

SCOOTER = "scooter"


def get_random_string(length):
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(length))


def get_random_mac():
    return rstr.xeger(r'[0-9A-F]{2}:[0-9A-F]{2}:[0-9A-F]{2}:[0-9A-F]{2}:[0-9A-F]{2}:[0-9A-F]{2}')


class Scooter:
    def __init__(self, id):
        self.AWSIoTMQTTClient = AWSIoTPyMQTT.AWSIoTMQTTClient(str(id))
        self.configure_mqtt()
        self.id = id
        self.battery_model = get_random_string(6)  # -> random battery model
        self.battery_cycle = 0
        self.last_known_point = (19.909286, 50.088594)
        self.last_telemetry = None
        self.mac = get_random_mac()
        self.ride = 0
        self.vehicle_type = 1
        self.user_id = 0

    def configure_mqtt(self):
        self.AWSIoTMQTTClient.configureEndpoint(ENDPOINT, 8883)
        self.AWSIoTMQTTClient.configureCredentials(PATH_TO_ROOT, PATH_TO_KEY, PATH_TO_CERT)
        self.AWSIoTMQTTClient.connect()

    def get_ride_id(self):
        return self.id + str(self.ride)

    def iterate_ride(self):
        self.ride += 1

    def send(self, message):
        print('scooter/{0}'.format(self.id), message)
        self.AWSIoTMQTTClient.publish('scooter/{0}'.format(self.id), message, 1)

    def set_user_id(self, user_id):
        self.user_id = user_id

    def disconnect(self):
        self.AWSIoTMQTTClient.disconnect()
