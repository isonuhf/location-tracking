#!/usr/bin/env python3
"""
Test script to simulate MQTT device messages
"""
import paho.mqtt.client as mqtt
import json
import time
from datetime import datetime

MQTT_BROKER = "localhost"
MQTT_PORT = 1883
MQTT_TOPIC = "devices/location"

def publish_device_location(client, device_id, latitude, longitude, battery=85, signal=-65):
    """Publish a device location message"""
    payload = {
        "device_id": device_id,
        "latitude": latitude,
        "longitude": longitude,
        "battery": battery,
        "signal_strength": signal,
        "status": "active",
        "timestamp": datetime.utcnow().isoformat() + "Z"
    }

    topic = f"{MQTT_TOPIC}/{device_id}"
    client.publish(topic, json.dumps(payload))
    print(f"Published: {device_id} at ({latitude}, {longitude})")

def main():
    client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION1)

    try:
        client.connect(MQTT_BROKER, MQTT_PORT, 60)
        client.loop_start()

        print("Connected to MQTT broker. Publishing test messages...")

        # Simulate multiple devices
        devices = [
            ("device_001", 39.9042, 116.4074),
            ("device_002", 39.9050, 116.4080),
            ("device_003", 39.9035, 116.4070),
        ]

        # Publish initial locations
        for device_id, lat, lon in devices:
            publish_device_location(client, device_id, lat, lon)
            time.sleep(0.5)

        # Simulate movement
        print("\nSimulating device movement...")
        for i in range(5):
            for device_id, lat, lon in devices:
                new_lat = lat + (i * 0.0001)
                new_lon = lon + (i * 0.0001)
                publish_device_location(client, device_id, new_lat, new_lon, battery=85-i*5)
                time.sleep(0.5)
            time.sleep(2)

        print("Test complete!")

    except Exception as e:
        print(f"Error: {e}")
    finally:
        client.loop_stop()
        client.disconnect()

if __name__ == "__main__":
    main()
