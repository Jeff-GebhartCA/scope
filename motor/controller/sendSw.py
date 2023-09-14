import network
import espnow
from machine import Pin
from time import sleep
from parallaxlcd import CharLCD

"""Run demo."""
# Initialize the LCD
lcd = CharLCD()
lcd.clear()
lcd.cursorOff()
lcd.print('PushCount: 0')
button=Pin(23,Pin.IN,pull=Pin.PULL_DOWN)

# A WLAN interface must be active to send()/recv()
sta = network.WLAN(network.STA_IF)  # Or network.AP_IF
sta.active(True)
# sta.disconnect()      # For ESP8266

e = espnow.ESPNow()
e.active(True)
peer = b'\xb0\xa7\x32\xf3\x48\x70'   # MAC address of peer's wifi interface
e.add_peer(peer)      # Must add_peer() before send()

butval = 0
pushcount = 0

e.send(peer, "Starting...")
while True:
    cmd = input("Enter Command: ")
    cmd_bytes = bytes(cmd,'utf-8')
    e.send(peer, cmd_bytes)        

        
    # sleep(0.01)
e.send(peer, b'end')