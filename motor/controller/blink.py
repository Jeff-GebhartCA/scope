from machine import Pin
from time import sleep

p=32

pin = Pin(32,Pin.OUT, pull=None)

while True:
    print("On")
    pin.value(1)
    sleep(1)
    print("Off")
    pin.value(0)
    sleep(1)
