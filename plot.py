import serial
import csv
import matplotlib.pyplot as plt

# =========================
# SETTINGS
# =========================

PORT = "COM7"
BAUD = 115200
CSV_FILE = "motor_throttle_log.csv"

# =========================
# DATA STORAGE
# =========================

times = []
m0 = []  # thumb
m1 = []  # palm
m2 = []  # index
m3 = []  # middle

# =========================
# SERIAL LOGGING
# =========================

ser = serial.Serial(PORT, BAUD, timeout=1)

print("Logging Pico motor data...")
print("Press Ctrl+C to stop, save, and plot.\n")

with open(CSV_FILE, "w", newline="") as f:
    writer = csv.writer(f)

    writer.writerow([
        "time_s",
        "thumb_percent",
        "palm_percent",
        "index_percent",
        "middle_percent"
    ])

    try:
        while True:
            line = ser.readline().decode(errors="ignore").strip()

            if not line:
                continue

            parts = line.split(",")

            if len(parts) != 5:
                print(line)
                continue

            try:
                row = [float(x) for x in parts]
            except ValueError:
                print(line)
                continue

            time_s = row[0]
            thumb = row[1]   # motor 0
            palm = row[2]    # motor 1
            index = row[3]   # motor 2
            middle = row[4]  # motor 3

            writer.writerow([time_s, thumb, palm, index, middle])
            f.flush()

            times.append(time_s)
            m0.append(thumb)
            m1.append(palm)
            m2.append(index)
            m3.append(middle)

            print(line)

    except KeyboardInterrupt:
        ser.close()
        print(f"\nSaved CSV file: {CSV_FILE}")

# =========================
# PLOT AFTER STOP
# =========================

if len(times) == 0:
    print("No valid motor data received. Check PORT and Pico output format.")
else:
    fig, axs = plt.subplots(4, 1, sharex=True, figsize=(10, 8))

    # Color scheme (clear + distinct)
    COLOR_THUMB = "blue"
    COLOR_INDEX = "green"
    COLOR_MIDDLE = "red"
    COLOR_PALM = "orange"

    # Top → bottom: thumb, index, middle, palm

    axs[0].plot(times, m0, color=COLOR_THUMB)
    axs[0].set_ylabel("Thumb (%)")
    axs[0].set_title("Thumb Motor")

    axs[1].plot(times, m2, color=COLOR_INDEX)
    axs[1].set_ylabel("Index (%)")
    axs[1].set_title("Index Motor")

    axs[2].plot(times, m3, color=COLOR_MIDDLE)
    axs[2].set_ylabel("Middle (%)")
    axs[2].set_title("Middle Motor")

    axs[3].plot(times, m1, color=COLOR_PALM)
    axs[3].set_ylabel("Palm (%)")
    axs[3].set_title("Palm Motor")

    axs[3].set_xlabel("Time (s)")

    for ax in axs:
        ax.grid(True)
        ax.set_ylim(-5, 105)

    fig.suptitle("Motor Throttle vs Time", fontsize=14)
    plt.tight_layout()
    plt.show()