import random
import time

from modules import comms

# from modules.mcp3008 import MCP3008 # Uncomment on Pi


def run(config, client):
    print(">> Sustainer Module: ONLINE")

    # adc = MCP3008() # Uncomment on Pi

    while True:
        # [SIMULATION] Generate fake moisture data
        moisture_level = random.randint(20, 80)

        # [HARDWARE] Uncomment on Pi
        # moisture_level = adc.read(0)

        msg = f"SOIL_LEVEL:{moisture_level}"
        comms.publish(client, config['mqtt']['topics']['biosphere'], msg)

        if moisture_level < 30:
            print(f"[SUSTAINER] Soil dry ({moisture_level}%). Watering...")
            # [HARDWARE] GPIO.output(pump_pin, GPIO.HIGH)
            time.sleep(2)
            # [HARDWARE] GPIO.output(pump_pin, GPIO.LOW)

        time.sleep(5)  # Check every 5 seconds
