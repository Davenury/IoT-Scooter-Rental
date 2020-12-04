import json
import paho.mqtt.client as mqtt

from Exceptions import WrongCommandException


class Telemetry:
    def __init__(self, battery: int, point):
        self.battery = battery
        self.point = point

    def get_telemetry(self):
        return json.dump(self.__dict__)


SCOOTER = "scooter"


class Scooter:
    def __init__(self):
        self.mqtt_client = mqtt.Client(id)
        self.mqtt_client.user_data_set(self)
        self.mqtt_client.on_connect = self.on_connect
        self.mqtt_client.on_message = self.on_message
        self.id = id
        self.mqtt_client.connect("test.mosquitto.org", 1883, 60)
        self.client_id = None
        self.battery = 0
        self.point = None

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

    def on_message(self):
        pass

    def publish(self, command_type: str):
        topic = self.get_topic(command_type)
        if command_type == "telemetry":
            payload = Telemetry(self.battery, self.point).get_telemetry()
            self.mqtt_client.publish(topic, payload)
        self.mqtt_client.publish(topic)

    # gdy w on_message dostaniemy potwierdzenie klienta
    def set_client_id(self, client_id: int):
        self.client_id = client_id

    # gdy w on_message dostaniemy koniec klienta
    def delete_client_id(self):
        self.client_id = None
