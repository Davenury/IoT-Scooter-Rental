import datetime
import random
import threading

from Scooter import Scooter, get_random_string
from Simulation import simulate, get_basic, Telemetry, get_zone, get_price

scooters = [Scooter(i+1) for i in range(10)]


def threading_fun(scooter):
    simulate(2010, 3, 10, 18, 25, 19, scooter)


if __name__ == "__main__":
    scooter = scooters[0]
    simulate(2020, 3, 10, 18, 25, 19, scooter)
    # for scooter in scooters:
    #     scooter.set_user_id(1)
    #     x = threading.Thread(target=threading_fun, args=(scooter,))
    #     x.start()
