import csv
import random
import time
from datetime import datetime

# Configurations
TOTAL_DURATION = 60  # total seconds to record (change as needed)
SESSION_LENGTH = 15  # how many seconds each label stays constant
FILENAME = "realistic_stress_mock.csv"
SUBJECT_COUNT = 3  # simulate different people

# CSV headers
headers = ["timestamp", "subject_id", "gsr", "bpm", "temperature", "accel_x", "accel_y", "accel_z", "label"]

# Write CSV header
with open(FILENAME, mode='w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(headers)

# Helpers
def add_noise(val, std=0.05):
    return round(val + random.gauss(0, std), 2)

def generate_shaky_accel(stressed):
    base = random.uniform(-0.2, 0.2)
    jitter = random.gauss(0, 0.3 if stressed else 0.05)
    return round(base + jitter, 2)

def generate_reading(stressed, subject_id):
    # Subject-specific bias (simulate person-to-person variation)
    bias = {
        "gsr": random.uniform(0.0, 0.2),
        "bpm": random.randint(-5, 5),
        "temp": random.uniform(-0.3, 0.3),
    }

    if stressed:
        gsr = add_noise(random.uniform(1.1, 1.5) + bias["gsr"], 0.05)
        bpm = random.randint(90, 110) + bias["bpm"]
        temp = round(random.uniform(34.0, 34.8) + bias["temp"], 2)
        ax = generate_shaky_accel(True)
        ay = generate_shaky_accel(True)
    else:
        gsr = add_noise(random.uniform(0.4, 0.9) + bias["gsr"], 0.03)
        bpm = random.randint(65, 85) + bias["bpm"]
        temp = round(random.uniform(35.0, 36.5) + bias["temp"], 2)
        ax = generate_shaky_accel(False)
        ay = generate_shaky_accel(False)

    az = round(random.uniform(9.4, 10.2), 2)
    return gsr, bpm, temp, ax, ay, az

# Data generation
def generate_data():
    print(f"Generating {TOTAL_DURATION} seconds of realistic auto-labeled mock data...")
    with open(FILENAME, mode='a', newline='') as file:
        writer = csv.writer(file)

        label_pattern = ["stressed", "not_stressed"] * (TOTAL_DURATION // (2 * SESSION_LENGTH))
        subject_id = random.randint(1, SUBJECT_COUNT)

        for label in label_pattern:
            for _ in range(SESSION_LENGTH):
                timestamp = datetime.now().isoformat()
                gsr, bpm, temp, ax, ay, az = generate_reading(stressed=(label == "stressed"), subject_id=subject_id)
                row = [timestamp, subject_id, gsr, bpm, temp, ax, ay, az, label]
                writer.writerow(row)
                print(row)
                time.sleep(1)  # comment this out if you want fast generation

generate_data()
