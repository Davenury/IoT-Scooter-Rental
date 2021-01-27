import random
import sys
sys.path.append("..")
import rstr
import string
import os
import AWSIoTPythonSDK.MQTTLib as AWSIoTPyMQTT
from geopy.distance import distance

from devices import battery_dict_file
from database.scooter_prepare import prepare_scooter

dir_path = os.path.dirname(os.path.realpath(__file__)) + "\\"
ENDPOINT = "a1r8jjr1mg7i8s-ats.iot.us-east-1.amazonaws.com"
# CLIENT_ID = "testDevice"
PATH_TO_CERT = "..\\certificates\\25ebfe00c3-certificate.pem.crt"
PATH_TO_KEY = "..\\certificates\\25ebfe00c3-private.pem.key"
PATH_TO_ROOT = "..\\certificates\\CA.pem"
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
    def __init__(self, id, are_certificates_necessary=False):
        self.AWSIoTMQTTClient = AWSIoTPyMQTT.AWSIoTMQTTClient(str(id))
        self.id = id
        self.battery_model = get_random_string(6)  # -> random battery model
        self.battery_cycle = 0
        self.last_known_point = (19.909286, 50.088594)
        self.last_telemetry = None
        self.mac = None
        self.ride = -1
        self.vehicle_type = 1
        self.user_id = -1
        prepare_scooter(self)
        if are_certificates_necessary:
            self.configure_mqtt()
        self.battery_drop_function = None
        self.battery_raise_temp_function = None

    def configure_mqtt(self):
        self.AWSIoTMQTTClient.configureEndpoint(ENDPOINT, 8883)
        self.AWSIoTMQTTClient.configureCredentials(PATH_TO_ROOT, PATH_TO_KEY, PATH_TO_CERT)
        self.AWSIoTMQTTClient.connect()

    def send(self, message):
        self.AWSIoTMQTTClient.publish('scooter/{0}'.format(self.id), message, 1)

    def set_user_id(self, user_id):
        self.user_id = user_id

    def disconnect(self):
        self.AWSIoTMQTTClient.disconnect()

    def send_begin(self, message):
        self.AWSIoTMQTTClient.publish('scooter/{0}/begin'.format(self.id), message, 1)

    def send_end(self, message):
        self.AWSIoTMQTTClient.publish('scooter/{0}/end_ride'.format(self.id), message, 1)

    def set_battery_drop_function(self, function):
        self.battery_drop_function = function

    def set_battery_raise_temp_function(self, function):
        self.battery_raise_temp_function = function

    def battery_drop_step(self, point):
        if self.battery_drop_function is None:
            km_distance = distance(point, self.last_known_point).km
            drop = 100 * km_distance / battery_dict_file.max_battery_distance_dict.\
                get(self.battery_model, battery_dict_file.DEFAULT_BATTERY_MAX_DISTANCE)
            return drop
        else:
            return self.battery_drop_function(self)

    def battery_raise_temp_step(self, step):
        if self.battery_raise_temp_function is None:
            return self.last_telemetry.battery_temp - step
        else:
            return self.battery_raise_temp_function(self)

    def get_left_kilometers(self):
        battery = self.last_telemetry.battery
        return battery * battery_dict_file.max_battery_distance_dict.\
            get(self.battery_model, battery_dict_file.DEFAULT_BATTERY_MAX_DISTANCE)
