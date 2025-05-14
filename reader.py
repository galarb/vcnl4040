from machine import Pin, I2C
from time import sleep
from VCNL4040 import VCNL4040

i2c = I2C(0, scl=Pin(21), sda=Pin(22), freq=400000)
sensor = VCNL4040(i2c)
sensor.dump_config()

for _ in range (100):
    prox = sensor.read_proximity()
    light = sensor.read_ambient_light()
    print("Proximity:", prox, " | Ambient Light:", light, "lux")
    sleep(0.5)

