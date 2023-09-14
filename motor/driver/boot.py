# This file is executed on every boot (including wake-boot from deepsleep)
#import esp
#esp.osdebug(None)
#import webrepl
#webrepl.start(
from time import sleep
from machine import Pin
led=Pin(2,Pin.OUT,pull=Pin.PULL_DOWN)
led.value(0)



# import listener
