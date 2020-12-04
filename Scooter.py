import json

import paho.mqtt.client as mqtt

from Exceptions import WrongCommandException


class Telemetry:
    def __init__(self, battery: float, point):
        self.battery = battery
        self.point = point

    def get_telemetry_to_publish(self):
        return json.dumps(self.__dict__)


SCOOTER = "scooter"


class Scooter:
    def __init__(self, id: int):
        self.mqtt_client = mqtt.Client(id)
        self.mqtt_client.user_data_set(self)
        self.mqtt_client.on_connect = self.on_connect
        self.mqtt_client.on_message = self.on_message
        self.id = id
        self.client_id = None
        self.mqtt_client.connect("test.mosquitto.org", 1883, 60)

        self.battery = 0
        self.point = None

    def get_topic(self, command_type: str):
        commands = {
            "start": f"{SCOOTER}/{self.id}/working",
            "telemetry": f"{SCOOTER}/{self.id}/telemetry",
            "end": f"{SCOOTER}/{self.id}/stopped_working"
        }
        if self.client_id is not None:
            commands["start_drive"] = f"{SCOOTER}/{self.id}/start/{self.client_id}"
            commands["end_drive"] = f"{SCOOTER}/{self.id}/end/{self.client_id}"

        if command_type not in commands.keys():
            raise WrongCommandException()
        return commands[command_type.lower()]

    def on_connect(self):
        self.mqtt_client.publish(self.get_topic("start"))

    def on_message(self):
        pass

    def publish(self, command_type: str):
        topic = self.get_topic(command_type)
        if command_type == "telemetry":
            payload = Telemetry(self.battery, self.point).get_telemetry_to_publish()
            self.mqtt_client.publish(topic, payload=payload)
        else:
            self.mqtt_client.publish(topic)

    # wykonujemy, gdy w on_message dostaniemy od serwera, że klient jest ok
    def set_client_id(self, client_id: int):
        self.client_id = client_id

    # wykonujemy, gdy w on_message otrzymamy, że użytkownik skończył jazdę
    def delete_client_id(self):
        self.client_id = None
