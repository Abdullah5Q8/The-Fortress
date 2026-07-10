import multiprocessing
import time

import yaml

from modules import caretaker, comms, sentinel, sustainer


# Load Configuration
def load_config():
    with open("config.yaml", "r") as f:
        return yaml.safe_load(f)


CONFIG = load_config()


# Wrapper functions for multiprocessing
def start_sentinel():
    client = comms.init_mqtt(CONFIG['mqtt']['broker'], CONFIG['mqtt']['port'], "Fortress_Sentinel")
    sentinel.run(CONFIG, client)


def start_caretaker():
    client = comms.init_mqtt(CONFIG['mqtt']['broker'], CONFIG['mqtt']['port'], "Fortress_Caretaker")
    caretaker.run(CONFIG, client)


def start_sustainer():
    client = comms.init_mqtt(CONFIG['mqtt']['broker'], CONFIG['mqtt']['port'], "Fortress_Sustainer")
    sustainer.run(CONFIG, client)


if __name__ == "__main__":
    print("🛡️  INITIALIZING THE FORTRESS OS...")

    # Hardware Setup (Mocking GPIO for Simulation)
    if CONFIG['system']['mode'] == "PRODUCTION":
        import RPi.GPIO as GPIO
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(CONFIG['gpio']['relay_lock'], GPIO.OUT)
        # Setup other pins...
    else:
        print("⚠️  RUNNING IN SIMULATION MODE (No Hardware IO)")

    # Start Processes
    processes = [
        multiprocessing.Process(target=start_sentinel, name="sentinel"),
        multiprocessing.Process(target=start_caretaker, name="caretaker"),
        multiprocessing.Process(target=start_sustainer, name="sustainer"),
    ]

    for p in processes:
        p.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n🛑 SHUTTING DOWN SYSTEMS...")
        for p in processes:
            p.terminate()
        if CONFIG['system']['mode'] == "PRODUCTION":
            GPIO.cleanup()
