import time

import paho.mqtt.client as mqtt
import streamlit as st
import yaml

# Load Config
with open("config.yaml", "r") as f:
    config = yaml.safe_load(f)


# MQTT Setup for Dashboard
def on_message(client, userdata, msg):
    # Update session state with new data
    topic = msg.topic
    payload = msg.payload.decode()
    if "security" in topic:
        st.session_state['security_status'] = payload
    elif "biosphere" in topic:
        st.session_state['soil_status'] = payload


def make_client(client_id):
    # paho-mqtt 1.x / 2.x compatible constructor
    try:
        return mqtt.Client(mqtt.CallbackAPIVersion.VERSION1, client_id)
    except AttributeError:
        return mqtt.Client(client_id)


client = make_client("Fortress_Dashboard")
client.on_message = on_message
client.connect(config['mqtt']['broker'], config['mqtt']['port'], 60)
client.subscribe(f"{config['mqtt']['topics']['security']}/#")
client.subscribe(f"{config['mqtt']['topics']['biosphere']}/#")
client.subscribe(config['mqtt']['topics']['security'])
client.subscribe(config['mqtt']['topics']['biosphere'])
client.loop_start()

# --- UI Layout ---
st.set_page_config(page_title="The Fortress", layout="wide")
st.title("🛡️ The Fortress: Command Center")

# Initialize State
if 'security_status' not in st.session_state:
    st.session_state['security_status'] = "SAFE"
if 'soil_status' not in st.session_state:
    st.session_state['soil_status'] = "SOIL_LEVEL: --"

# Top Metrics
col1, col2, col3 = st.columns(3)

status_color = "normal" if st.session_state['security_status'] == "SAFE" else "inverse"
col1.metric("System Status", st.session_state['security_status'], delta_color=status_color)
col2.metric("Next Prayer", "Maghrib", "17:45")  # Placeholder
col3.metric("Biosphere", st.session_state['soil_status'])

st.markdown("---")

# Controls
c1, c2 = st.columns(2)
with c1:
    st.subheader("🔒 Security Override")
    if st.button("TRIGGER LOCKDOWN", type="primary"):
        client.publish(config['mqtt']['topics']['security'], "LOCKDOWN_MANUAL")
        st.error("LOCKDOWN SIGNAL SENT")

with c2:
    st.subheader("☀️ Routine Override")
    if st.button("Open Curtains"):
        client.publish(config['mqtt']['topics']['automation'], "CURTAINS_OPEN")
        st.success("Opening...")

# Auto-refresh loop (Streamlit specific trick)
time.sleep(1)
st.rerun()
