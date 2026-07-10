import datetime
import time

import requests

from modules import comms


def get_prayer_times(lat, long):
    try:
        url = f"http://api.aladhan.com/v1/timings?latitude={lat}&longitude={long}&method=4"
        res = requests.get(url, timeout=5).json()
        return res['data']['timings']
    except Exception:
        return None


def run(config, client):
    print(">> Caretaker Module: ONLINE")

    # State tracking
    prayer_times = get_prayer_times(config['location']['lat'], config['location']['long'])
    last_check = datetime.datetime.now().day

    while True:
        now = datetime.datetime.now()
        current_time_str = now.strftime("%H:%M")

        # Refresh API daily
        if now.day != last_check:
            prayer_times = get_prayer_times(config['location']['lat'], config['location']['long'])
            last_check = now.day

        # --- Faith Logic ---
        if prayer_times:
            for prayer, p_time in prayer_times.items():
                if current_time_str == p_time:
                    print(f"[CARETAKER] It is {prayer} time. Muting media.")
                    comms.publish(client, config['mqtt']['topics']['automation'], f"PRAYER_{prayer.upper()}")
                    time.sleep(60)  # Prevent multiple triggers

        # --- Morning Routine (Mock) ---
        if current_time_str == "06:00":  # Example sunrise
            print("[CARETAKER] Good Morning. Opening Curtains.")
            # [HARDWARE] stepper_motor.step(2000)
            time.sleep(60)

        time.sleep(10)  # Check every 10 seconds
