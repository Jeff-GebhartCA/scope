import utime
from machine import I2C, Pin
from mpu9250 import MPU9250
from mpu6500 import MPU6500, SF_G, SF_DEG_S
from math import atan2,sqrt

i2c = I2C(scl=Pin(22), sda=Pin(21))
mpu6500 = MPU6500(i2c, accel_sf=SF_G, gyro_sf=SF_DEG_S)
sensor = MPU9250(i2c, mpu6500=mpu6500)

print("MPU9250 id: " + hex(sensor.whoami))

while True:
    print(f"Accel: {sensor.acceleration}")
    taccel = sqrt(float(sensor.acceleration[0])**2+float(sensor.acceleration[1])**2+float(sensor.acceleration[2])**2)
    print(f"Total Accel: {taccel}")
    print(f"Gyro: {sensor.gyro}")
    print(f"Mag: {sensor.magnetic}")
    print(f"Heading: {atan2(sensor.magnetic[1],sensor.magnetic[0])}")
    print(f"Temp: {sensor.temperature}")
    print("-"* 80)

    utime.sleep_ms(2000)