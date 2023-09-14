from machine import Pin
from time import sleep

p=23

pin = Pin(p,Pin.IN,pull=Pin.PULL_DOWN)

while True:
    print(pin.value())
    sleep(.1)