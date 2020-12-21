from time import sleep

from Scooter import Scooter

scooter = Scooter(2)
while True:
    scooter.send()
    scooter.receive()
    sleep(1)
