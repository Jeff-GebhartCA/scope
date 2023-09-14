from esp32 import RMT
from machine import Pin,PWM
from time import sleep
import net

# Pin numbers
EN=32
MS1=33
MS2=25
MS3=26
RST=27
SLP=14
STEP=23
DIR=13
STEPSPERREV=200
MICROSTEP = 32
FREQ=(MICROSTEP * STEPSPERREV) /60
CLOCK_FREQ = 80_000_000
CLOCK_DIVIDER = 100

net.activate()
net.status()
import time
from ntptime import settime
timeset = False
while not timeset:
    try:
        settime()
        timeset=True
    except Exception as e:
        print(e)
        pass
print(time.localtime())

r=RMT(0,pin=Pin(STEP),clock_div=CLOCK_DIVIDER)
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