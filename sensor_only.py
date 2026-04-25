from machine import Pin, I2C
import time

i2c = I2C(1, scl=Pin(27), sda=Pin(26), freq=400000)

ADS1115_ADDR = 0x48
REG_CONVERSION = 0x00
REG_CONFIG = 0x01

LSB_SIZE = 4.096 / 32768  # gain ±4.096V


def write_register(reg, value):
    i2c.writeto(ADS1115_ADDR, bytes([
        reg,
        (value >> 8) & 0xFF,
        value & 0xFF
    ]))


def read_register(reg):
    i2c.writeto(ADS1115_ADDR, bytes([reg]))
    data = i2c.readfrom(ADS1115_ADDR, 2)
    value = (data[0] << 8) | data[1]
    if value > 32767:
        value -= 65536
    return value


def read_channel(ch):
    mux = {
        0: 0x4000,  # A0
        1: 0x5000,  # A1
        2: 0x6000,  # A2
        3: 0x7000   # A3
    }

    config = (
        0x8000 |        # start conversion
        mux[ch] |
        0x0200 |        # gain ±4.096V
        0x0100 |        # single-shot
        0x0080 |        # 128 SPS
        0x0003
    )

    write_register(REG_CONFIG, config)
    time.sleep(0.01)

    raw = read_register(REG_CONVERSION)
    voltage = raw * LSB_SIZE
    return raw, voltage


while True:
    values = []

    for ch in range(4):
        raw, volt = read_channel(ch)
        values.append(f"A{ch}: {raw} ({volt:.2f}V)")

    print(" | ".join(values))

    time.sleep(0.5)  # slower update (adjust here)