import random
import threading
import sys
sys.path.append("..")
from devices.Scooter import Scooter
from simulation.Simulation import simulate

scooters = [Scooter(i+1, False) for i in range(10)] # change False to True, when you'll change mode to send


def threading_fun(scooter):
    simulate(scooter, mode="print")


if __name__ == "__main__":
    for scooter in scooters:
        # threading_fun(scooter)
        x = threading.Thread(target=threading_fun, args=(scooter,))
        x.start()
