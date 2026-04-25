from machine import Pin, PWM
import sys

# Motor pins (ULN2803A inputs)
motor_pins = [2, 3, 4, 5]

motors = []
for pin_num in motor_pins:
    pwm = PWM(Pin(pin_num))
    pwm.freq(1000)  # 1 kHz PWM
    pwm.duty_u16(0)
    motors.append(pwm)

def set_motor(index, voltage):
    """
    index: 0-3
    voltage: 0.0 - 3.3 (mapped to PWM duty)
    """
    if index < 0 or index > 3:
        print("Invalid motor index (0-3)")
        return

    if voltage < 0 or voltage > 3.3:
        print("Voltage must be between 0 and 3.3")
        return

    duty = int((voltage / 3.3) * 65535)
    motors[index].duty_u16(duty)

def all_off():
    for m in motors:
        m.duty_u16(0)

print("Ready. Enter: motor_index voltage")
print("Example: 1 2.5  (motor 1 at ~2.5V strength)")
print("Type 'off' to stop all motors.")

while True:
    try:
        cmd = input(">> ").strip()

        if cmd.lower() == "off":
            all_off()
            print("All motors OFF")
            continue

        parts = cmd.split()
        if len(parts) != 2:
            print("Format: <motor 0-3> <voltage 0-3.3>")
            continue

        motor_idx = int(parts[0])
        voltage = float(parts[1])

        set_motor(motor_idx, voltage)
        print(f"Motor {motor_idx} set to {voltage}V equivalent")

    except Exception as e:
        print("Error:", e)