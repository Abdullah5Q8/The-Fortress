# 🛡️ The Fortress — Context-Aware Home OS

A custom-engineered, decentralized home operating system that prioritizes physical
security, data privacy, and lifestyle alignment. Unlike passive hubs (Alexa/Google
Home), The Fortress is proactive: computer vision for threat assessment, hard-coded
logic for religious and routine synchronization, and closed-loop biosphere control —
all running locally on a Raspberry Pi 5, no cloud required.

Full write-up: [`Description.pdf`](Description.pdf) ·
Hardware diagrams: [`Hardware Architecture Visualization.pdf`](Hardware%20Architecture%20Visualization.pdf)

## Architecture

Three microservices orchestrated by `main.py` (one process each), talking over MQTT:

| Module | File | Responsibility |
|---|---|---|
| **The Sentinel** | `modules/sentinel.py` | YOLOv8 object recognition — detects threats (not just motion) and triggers physical lockdown hardware |
| **The Caretaker** | `modules/caretaker.py` | Prayer-time (Adhan) automation via the AlAdhan API, morning curtain routine, circadian control |
| **The Sustainer** | `modules/sustainer.py` | Soil-moisture monitoring (MCP3008 ADC) with closed-loop irrigation and pet feeding |

Supporting pieces: `modules/comms.py` (MQTT handler), `modules/mcp3008.py`
(SPI bridge for analog sensors), `dashboard/app.py` (Streamlit command center).

## Quick Start (Simulation — any machine)

```bash
pip install -r requirements.txt   # comment out spidev / RPi.GPIO off-Pi
python main.py                    # config.yaml mode is SIMULATION by default
```

Optional extras:

```bash
# Local MQTT broker (otherwise modules run standalone without messaging)
sudo apt install mosquitto && sudo systemctl start mosquitto

# Command center UI
streamlit run dashboard/app.py
```

## Deploying to the Raspberry Pi

1. Set `system.mode: "PRODUCTION"` in `config.yaml`
2. Install `spidev` and `RPi.GPIO` (already in `requirements.txt`)
3. Wire per the BCM pin map in `config.yaml` (`relay_lock: 17`, `relay_shaker: 27`,
   `servo_feeder: 18`, `stepper_pins: [22, 23, 24, 25]`)
4. Uncomment the `[HARDWARE]` lines in each module

## Roadmap

- [x] Phase 0 — Architecture, docs, and hardware design
- [x] Phase 1 — Code scaffold: orchestrator, all three modules, dashboard
- [ ] Phase 2 — Run full simulation with MQTT broker + dashboard end-to-end
- [ ] Phase 3 — Pi deployment: GPIO relay/servo wiring, MCP3008 soil sensor
- [ ] Phase 4 — Sentinel tuning: custom threat classes, sub-200ms inference
- [ ] Phase 5 — Caretaker hardware: stepper curtain control, sleep tracking
- [ ] Phase 6 — Hardening: watchdog restarts, logging, offline prayer-time fallback
