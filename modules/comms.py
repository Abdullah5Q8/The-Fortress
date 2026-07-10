import paho.mqtt.client as mqtt


def _make_client(client_id):
    # paho-mqtt 2.x changed the constructor signature; support both so
    # `pip install paho-mqtt` works whether it resolves to 1.x or 2.x
    try:
        return mqtt.Client(mqtt.CallbackAPIVersion.VERSION1, client_id)
    except AttributeError:
        return mqtt.Client(client_id)


def init_mqtt(broker, port=1883, client_id="Fortress_Brain"):
    client = _make_client(client_id)
    try:
        client.connect(broker, port, 60)
        client.loop_start()
        print(f"[MQTT] Connected to {broker}")
        return client
    except Exception as e:
        print(f"[MQTT] Connection Failed: {e}")
        return None


def publish(client, topic, message):
    if client:
        client.publish(topic, message)
        # print(f"[MQTT Tx] {topic}: {message}") # Uncomment for debug
