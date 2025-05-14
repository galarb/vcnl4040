import time
from machine import I2C

class VCNL4040:
    I2C_ADDR = 0x60

    REG_PS_DATA = 0x08
    REG_ALS_DATA = 0x09
    REG_ALS_CONF = 0x00
    REG_PS_CONF1_2 = 0x03
    REG_PS_CONF3_MS = 0x04
    REG_PS_THDL = 0x06
    REG_PS_THDH = 0x07

    def __init__(self, i2c):
        self.i2c = i2c
        self.init_sensor()

    def write16(self, reg, value):
        buf = bytearray(2)
        buf[0] = value & 0xFF
        buf[1] = (value >> 8) & 0xFF
        self.i2c.writeto_mem(self.I2C_ADDR, reg, buf)

    def read16(self, reg):
        data = self.i2c.readfrom_mem(self.I2C_ADDR, reg, 2)
        return data[1] << 8 | data[0]

    def init_sensor(self):
        # Enable ambient light sensing (ALS)
        self.write16(self.REG_ALS_CONF, 0x0010)  # ALS_IT=80ms, ALS_EN=1

        # Enable proximity sensing (PS)
        self.write16(self.REG_PS_CONF1_2, 0x030D)  # PS_SD=0 (enabled), PS_IT=01, PS_PERS=1

        # Configure IR LED and measurement settings
        self.write16(self.REG_PS_CONF3_MS, 0x0048)  # PS_MS=0x48 (standard settings, LED on)

        # Set proximity threshold low and high (optional)
        self.write16(self.REG_PS_THDL, 0x0000)
        self.write16(self.REG_PS_THDH, 0xFFFF)

    def read_ambient_light(self):
        return self.read16(self.REG_ALS_DATA)

    
    def read_proximity(self):
        raw = self.i2c.readfrom_mem(self.I2C_ADDR, self.REG_PS_DATA, 2)
        value = raw[1] << 8 | raw[0]
        return value

    def dump_config(self):
        conf1_2 = self.read16(self.REG_PS_CONF1_2)
        conf3 = self.read16(self.REG_PS_CONF3_MS)
        print(f"PS_CONF1_2: 0x{conf1_2:04X}")
        print(f"PS_CONF3_MS: 0x{conf3:04X}")

