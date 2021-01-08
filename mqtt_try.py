from Scooter import Scooter
import os

if __name__ == "__main__":
    scooter = Scooter(1)
    scooter2 = Scooter(2)
    for i in range(1, 10):
        scooter.send("Tryout")
        scooter2.send("Tryout")
