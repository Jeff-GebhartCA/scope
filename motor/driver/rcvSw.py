import network
import espnow
from machine import Pin

# A WLAN interface must be active to send()/recv()
sta = network.WLAN(network.STA_IF)
sta.active(True)
# sta.disconnect()   # Because ESP8266 auto-connects to last Access Point

e = espnow.ESPNow()
e.active(True)
led = Pin(2,Pin.OUT)
led.value(0)

while True:
    host, msg = e.recv()
    if msg:             # msg == None if timeout in recv()
        print(host, msg)
        if msg == b'Button: 1':
            led.value(1)
        else:
            led.value(0)
        if msg == b'end':
            break