import time

from modules import comms


def run(config, client):
    print(">> Sentinel Module: ONLINE")

    try:
        import cv2
        from ultralytics import YOLO
    except ImportError as e:
        print(f"[SENTINEL] Vision stack unavailable ({e}). Falling back to heartbeat mode.")
        _run_headless(config, client)
        return

    # Load Model (Downloads automatically on first run)
    model = YOLO(config['camera']['model_path'])
    cap = cv2.VideoCapture(config['camera']['index'])

    if not cap.isOpened():
        print("[SENTINEL] No camera found. Falling back to heartbeat mode.")
        _run_headless(config, client)
        return

    # Threat Classes (COCO dataset indices)
    # 43: Knife, 67: Cell Phone (for testing), 0: Person
    THREAT_CLASSES = [43, 67]

    while True:
        ret, frame = cap.read()
        if not ret:
            time.sleep(1)
            continue

        # Inference
        results = model.predict(frame, conf=0.5, verbose=False, imgsz=320)

        threat_detected = False
        for r in results:
            for box in r.boxes:
                cls = int(box.cls[0])
                if cls in THREAT_CLASSES:
                    threat_detected = True
                    label = model.names[cls]

                    # --- ACTION PROTOCOL ---
                    msg = f"THREAT DETECTED: {label}"
                    print(f"!!! [SENTINEL] {msg} !!!")
                    comms.publish(client, config['mqtt']['topics']['security'], "LOCKDOWN")

                    # [HARDWARE] Uncomment on Pi
                    # GPIO.output(config['gpio']['relay_lock'], GPIO.HIGH)

        if not threat_detected:
            # Heartbeat to dashboard
            comms.publish(client, config['mqtt']['topics']['security'], "SAFE")

        # Optional: Show feed (Disable on headless Pi)
        # cv2.imshow('Sentinel Eye', results[0].plot())
        # if cv2.waitKey(1) == ord('q'): break

        time.sleep(0.5)  # Throttle to save CPU


def _run_headless(config, client):
    # Keeps the security heartbeat alive on machines with no camera so the
    # rest of the system (dashboard, lockdown wiring) can still be tested
    while True:
        comms.publish(client, config['mqtt']['topics']['security'], "SAFE")
        time.sleep(2)
