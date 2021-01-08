import threading

from Scooter import Scooter, get_random_string
from Simulation import simulate

scooters = [Scooter(i) for i in range(10)]


def threading_fun(scooter):
    simulate(2010, 3, 10, 18, 25, 19, scooter)


if __name__ == "__main__":
    for scooter in scooters:
        x = threading.Thread(target=threading_fun, args=(scooter,))
        x.start()
