import random
import threading

from devices.Scooter import Scooter
from simulation.Simulation import simulate

scooters = [Scooter(i+1) for i in range(10)]


def threading_fun(scooter):
    day = random.randint(1, 31)
    hour = random.randint(0, 23)
    minute = random.randint(0, 59)
    second = random.randint(0, 59)
    simulate(2020, 3, day, hour, minute, second, scooter)


if __name__ == "__main__":
    for scooter in scooters:
        # threading_fun(scooter)
        x = threading.Thread(target=threading_fun, args=(scooter,))
        x.start()
