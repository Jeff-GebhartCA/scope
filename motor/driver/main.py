from machine import Pin
from time import sleep

boot = Pin(0,Pin.IN)
for i in range(5):
    led.value(1)
    sleep(0.5)
    led.value(0)
    sleep(0.5)
if boot.value():
    import listener
