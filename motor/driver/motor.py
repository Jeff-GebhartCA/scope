from esp32 import RMT
from machine import Pin,PWM
from time import sleep
import network
import espnow
# import net

# Pin numbers
RAEN=25
RADIR=26
RASTEP=27

DECEN=19
DECDIR=18
DECSTEP=16


EN=32
MS1=33
MS2=25
MS3=26
RST=27
SLP=14
STEP=RASTEP
DIR=13
STEPSPERREV=200
MICROSTEP = 16
FREQ=(MICROSTEP * STEPSPERREV) /60
CLOCK_FREQ = 80_000_000
CLOCK_DIVIDER = 255

class Motor:

    def __init__(self,EN=RAEN,DIR=RADIR,STEP=RASTEP,Speed=0,RMTNum=0):
        self.EN,self.DIR,self.STEP,self.SPEED,self.RMTNum = EN,DIR,STEP,Speed,RMTNum

        # Init Pins
        self.EN_Pin = Pin(EN,Pin.OUT,pull=Pin.PULL_DOWN)
        self.EN_Pin.value(0)
        self.DIR_Pin = Pin(DIR,Pin.OUT,pull=Pin.PULL_DOWN)
        self.DIR_Pin.value(0)
        self.STEP_Pin = Pin(STEP,Pin.OUT,pull=Pin.PULL_DOWN)
        self.STEP_Pin.value(0)
        self.pulses=RMT(self.RMTNum,pin=self.STEP_Pin,clock_div=CLOCK_DIVIDER)

        if Speed > 0:
            self.start(Speed)

            
    def start(self,Speed):
        
        if Speed % 2 == 0:
            pulse_def = (int(Speed/2),int(Speed/2))
        else:
            pulse_def = (int(Speed/2),int(Speed/2)+1)
        
        self.EN_Pin.value(1)
        self.pulses.loop(True)
        self.pulses.write_pulses(pulse_def)

    def speed(self,Speed):
        
        if Speed % 2 == 0:
            pulse_def = (int(Speed/2),int(Speed/2))
        else:
            pulse_def = (int(Speed/2),int(Speed/2)+1)
        
        # self.EN_Pin.value(1)
        self.pulses.loop(True)
        self.pulses.write_pulses(pulse_def)
    def stop(self):
        self.pulses.loop(False)
    
    def disable(self):
        self.EN_Pin.value(0)
    
    def enable(self):
        self.EN_Pin.value(1)
    
    def forward(self):
        self.DIR_Pin.value(0)
    
    def back(self):
        self.DIR_Pin.value(1)

        
def timeTest(m,seconds=60):
    m.enable()
    for i in range(seconds):
        print (i)
        sleep(1)
    m.disable()





        




# A WLAN interface must be active to send()/recv()
sta = network.WLAN(network.STA_IF)
sta.active(True)
# sta.disconnect()   # Because ESP8266 auto-connects to last Access Point

e = espnow.ESPNow()
e.active(True)
led = Pin(2,Pin.OUT)
led.value(0)

# net.activate()
# net.status()
import time
# from ntptime import settime
# timeset = False
# while not timeset:
#     try:
#         settime()
#         timeset=True
#     except Exception as e:
#        print(e)
#         pass
# print(time.localtime())

# r=RMT(0,pin=Pin(RASTEP),clock_div=CLOCK_DIVIDER)
sleeptime=1
def rev(revs=1):
    motor = PWM(Pin(STEP,Pin.OUT,pull=Pin.PULL_UP),freq=FREQ,duty_u16=32768)
    sleep(60)
    motor.deinit()

def m(mpr=1,time=60,debug=False):
    return set_mpr(mpr,time,debug)

def set_mpr(mpr=1,time=60,debug=False):
    global r
    clock_divider = CLOCK_DIVIDER
    clock_period_ms = (1/CLOCK_FREQ/clock_divider)*1e7
    print(f"Clock period ms: {clock_period_ms}")

    micro_step_per_rev = STEPSPERREV * MICROSTEP
    seconds_per_period = mpr * 60
    miliseconds_per_microstep = (seconds_per_period/micro_step_per_rev) * 1000

    print(f"Milliseconds Per Microstep: {miliseconds_per_microstep}")
    ticks_per_cycle = miliseconds_per_microstep/clock_period_ms
    pulse_ticks = int(ticks_per_cycle/2)
    print(f"Pulse Ticks: {pulse_ticks}")

    
    print("Beginning...")
    if not debug:
        r.loop(True)
        r.write_pulses((pulse_ticks,pulse_ticks))
    print("Started")
    sleep(time)
    r.loop(False)
    print("Done")
    
def bat():
    global r
    print("Begin...")
    print (time.localtime())
    p=Pin(15,Pin.IN,pull=Pin.PULL_DOWN)
    while not p.value():
        print("Please insert battery")
        sleep(1)
    print(f"Start Time: {time.localtime()}")
    r.loop(True)
    r.write_pulses((30000,30000))
    while p.value():
        sleep(1)
    r.loop(False)
    print(f"End time: {time.localtime()}")

def start_motor():
    global r
    r.loop(True)
    r.write_pulses((30000,30000))

def stop_motor():
    r.loop(False)
    
def rcv_button():
    global e,r,led

    while True:
        host,msg = e.recv()
        if msg:
            print(host,msg)
            if msg== b'Button: 1':
                if led.value()==0:
                    led.value(1)
                    start_motor()
            else:
                if led.value():
                    led.value(0)
                    stop_motor()




