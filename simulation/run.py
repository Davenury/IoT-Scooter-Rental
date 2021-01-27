import random
import threading
import sys
sys.path.append("..")
from devices.Scooter import Scooter
from simulation.Simulation import simulate

scooters = [Scooter(i+1) for i in range(10)]


def threading_fun(scooter):
    simulate(scooter, mode="print")


if __name__ == "__main__":
    for scooter in scooters:
        # threading_fun(scooter)
        x = threading.Thread(target=threading_fun, args=(scooter,))
        x.start()
