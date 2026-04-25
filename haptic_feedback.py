from machine import Pin, I2C, PWM
import time

# =========================
# ADS1115 SETUP
# =========================

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
        3: 0x4000,  # A3 = motor 0, reversed
        2: 0x5000,  # A2 = motor 1
        1: 0x6000,  # A1 = motor 2
        0: 0x7000   # A0 = motor 3
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


# =========================
# HAPTIC MOTOR SETUP
# =========================

motor_pins = [2, 3, 4, 5]  # GP pins 2-5

motors = []

for pin_num in motor_pins:
    pwm = PWM(Pin(pin_num))
    pwm.freq(1000)
    pwm.duty_u16(0)
    motors.append(pwm)


# =========================
# FSR TO MOTOR MAPPING
# =========================

NO_TOUCH_VOLTAGE = 3.3
FULL_PRESS_VOLTAGE = 0.2

MAX_DUTY = 65535
MIN_DUTY = 0


def voltage_to_duty(voltage):
    """
    Higher voltage = less pressure = less vibration
    Lower voltage = more pressure = more vibration
    """

    # Clamp voltage
    if voltage > NO_TOUCH_VOLTAGE:
        voltage = NO_TOUCH_VOLTAGE

    if voltage < FULL_PRESS_VOLTAGE:
        voltage = FULL_PRESS_VOLTAGE

    # Invert mapping
    strength = (NO_TOUCH_VOLTAGE - voltage) / (NO_TOUCH_VOLTAGE - FULL_PRESS_VOLTAGE)

    duty = int(strength * MAX_DUTY)

    return duty


def all_off():
    for motor in motors:
        motor.duty_u16(0)


# =========================
# MAIN LOOP
# =========================

try:
    while True:
        print_values = []

        for ch in range(4):
            raw, voltage = read_channel(ch)

            duty = voltage_to_duty(voltage)
            motors[ch].duty_u16(duty)

            percent = (duty / 65535) * 100

            print_values.append(
                f"Sensor {ch}: {voltage:.2f}V -> Motor {ch}: {percent:.0f}%"
            )

        print(" | ".join(print_values))

        time.sleep(0.05)

except KeyboardInterrupt:
    all_off()
    print("Stopped. All motors OFF.")