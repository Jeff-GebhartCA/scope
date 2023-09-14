import network
import espnow
from machine import Pin

from motor import (
    Motor,
    RAEN,RADIR,RASTEP,
    DECEN,DECDIR,DECSTEP
)

# A WLAN interface must be active to send()/recv()
sta = network.WLAN(network.STA_IF)
sta.active(True)
# sta.disconnect()   # Because ESP8266 auto-connects to last Access Point

e = espnow.ESPNow()
e.active(True)
led = Pin(2,Pin.OUT)
led.value(0)

#    def __init__(self,EN=RAEN,DIR=RADIR,STEP=RASTEP,Speed=0,RMTNum=0):

# Set up motor driver objects
ra = Motor(RAEN,RADIR,RASTEP,RMTNum=0)
dec = Motor(DECEN,DECDIR,DECSTEP,RMTNum=1)
print("Listening for commands...")
bootpin = Pin(0,Pin.IN)
while bootpin.value():
    host,msg = e.recv()
    if msg:
        msg=str(msg.decode("utf-8"))
        # print(msg)
        parsemsg = msg.split(" ")
        if len(parsemsg) > 1 and len(parsemsg) <= 3:
            motor = parsemsg[0].upper()
            command = parsemsg[1].upper()
            if len(parsemsg) == 3:
                arg = int(parsemsg[2])
            else:
                arg = None
            print(f"Motor: {motor}\tCommand: {command}\tArg:{arg}")

            if motor == "RA":
                if command == "EN":
                    ra.enable()
                elif command == "DIS":
                    ra.disable()
                elif command == "FWD":
                    ra.forward()
                elif command == "BACK":
                    ra.back()
                elif command == "SPEED":
                    ra.speed(arg)
                elif command == "STOP":
                    ra.stop()
                elif command == "LED":
                    led.value(arg)
                else:
                    print("Invalid Command")
                
            elif motor == "DEC":
                if command == "EN":
                    dec.enable()
                elif command == "DIS":
                    dec.disable()
                elif command == "FWD":
                    dec.forward()
                elif command == "BACK":
                    dec.back()
                elif command == "SPEED":
                    dec.speed(arg)
                elif command == "STOP":
                    dec.stop()
                elif command == "LED":
                    led.value(arg)
                else:
                    print("Invalid Command")                
            else:
                print("Invalid Motor")
ra.disable()
dec.disable()

for i in range(5):
    
    led.value(1)
    sleep(0.1)
    led.value(0)
    sleep(0.1)
