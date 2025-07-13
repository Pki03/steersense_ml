import csv
import random
import time
from datetime import datetime

FILENAME = "realistic_drowsiness_mock.csv"
TOTAL_DURATION = 90  # seconds
headers = ["timestamp", "EAR", "MOR", "neck_tilt", "label"]

# Helper: Add noise but stay within range
def jitter(value, min_val, max_val, std=0.01):
    noisy = value + random.gauss(0, std)
    return round(min(max(noisy, min_val), max_val), 3)

# Simulated state control
def simulate_state_block(state="awake"):
    """
    Generate realistic values based on the current state
    """
    if state == "awake":
        base_ear = 0.3
        base_mor = 0.3
        base_tilt = 10
    elif state == "drowsy":
        base_ear = 0.21
        base_mor = 0.65
        base_tilt = 18
    else:  # micro sleep (eyes closed)
        base_ear = 0.15
        base_mor = 0.35
        base_tilt = 20

    # Apply small jitter
    ear = jitter(base_ear, 0.1, 0.35, 0.02)
    mor = jitter(base_mor, 0.2, 0.9, 0.05)
    tilt = round(base_tilt + random.gauss(0, 2), 2)

    # Labeling logic
    if ear < 0.22 or mor > 0.6 or tilt > 15:
        label = "drowsy"
    else:
        label = "not_drowsy"

    return ear, mor, tilt, label

# Simulate data
print(f"⏳ Generating {TOTAL_DURATION} seconds of realistic mock drowsiness data...")
with open(FILENAME, mode='w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(headers)

    current_state = "awake"
    state_timer = random.randint(10, 20)  # seconds to stay in current state

    for i in range(TOTAL_DURATION):
        if state_timer == 0:
            # Randomly flip state (simulate fatigue cycles)
            current_state = random.choices(
                ["awake", "drowsy", "microsleep"],
                weights=[0.6, 0.3, 0.1]
            )[0]
            state_timer = random.randint(8, 15)

        ear, mor, tilt, label = simulate_state_block(current_state)

        # Occasionally blink (simulate very low EAR for 1 second)
        if current_state == "awake" and random.random() < 0.05:
            ear = 0.15

        timestamp = datetime.now().isoformat()
        writer.writerow([timestamp, ear, mor, tilt, label])
        print([timestamp, ear, mor, tilt, label])

        state_timer -= 1
        time.sleep(1)  # Remove this line for instant generation

print(f"\n✅ Done! Data saved to: {FILENAME}")
