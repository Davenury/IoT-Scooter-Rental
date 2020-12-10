import json
import paho.mqtt.client as mqtt

from Exceptions import WrongCommandException

SCOOTER = "scooter"


class Scooter:
    def __init__(self):
        self.mqtt_client = mqtt.Client(id)
        self.mqtt_client.user_data_set(self)
        self.mqtt_client.on_connect = self.on_connect
        self.mqtt_client.on_message = self.on_message
        self.id = id
        self.mqtt_client.connect("test.mosquitto.org", 1883, 60)
        self.battery = 0

    def get_topic(self, command_type: str):
        command_type = command_type.lower()
        commands = {
            "start": f"{SCOOTER}/{self.id}/working",
            "end": f"{SCOOTER}/{self.id}/end_working",
            "telemetry": f"{SCOOTER}/{self.id}/telemetry"
        }
        if self.client_id is not None:
            commands["start_drive"] = f"{SCOOTER}/{self.id}/start/{self.client_id}"
            commands["end_drive"] = f"{SCOOTER}/{self.id}/end/{self.client_id}"
        if command_type not in commands.keys():
            raise WrongCommandException()
        return commands[command_type]

    def on_connect(self):
        self.mqtt_client.publish(self.get_topic("start"))

    # potwierdzenie od serwera, że client jest ok
    def on_message(self):
        pass

    def publish(self, command_type: str, item=None):
        topic = self.get_topic(command_type)
        if command_type == "telemetry":
            self.mqtt_client.publish(topic, item)
        self.mqtt_client.publish(topic)

    # gdy w on_message dostaniemy potwierdzenie klienta
    def set_client_id(self, client_id: int):
        self.client_id = client_id

    # gdy w on_message dostaniemy koniec klienta
    def delete_client_id(self):
        self.client_id = None
