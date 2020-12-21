import zmq

from Exceptions import WrongCommandException

SCOOTER = "scooter"


class Scooter:
    def __init__(self, id):
        self.init_zmq()
        self.id = id
        self.client_id = None
        self.battery_model = "dsadsa"  # -> random battery model
        self.battery_circle = 0
        self.last_known_point = (19.909286, 50.088594)
        self.last_telemetry = None

    def init_zmq(self):
        self.context = zmq.Context()
        self.socket = self.context.socket(zmq.REQ)
        self.socket.connect("tcp://localhost:5555")

    def send(self, message):
        self.socket.send_json(message)

    def receive(self):
        message = self.socket.recv()
        print(message)

    # gdy w on_message dostaniemy potwierdzenie klienta
    def set_client_id(self, client_id: int):
        self.client_id = client_id

    # gdy w on_message dostaniemy koniec klienta
    def delete_client_id(self):
        self.client_id = None
