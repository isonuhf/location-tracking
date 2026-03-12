import paho.mqtt.client as mqtt
import json
import asyncio
from datetime import datetime
from config import settings
from database import SessionLocal, DeviceLocation
from websocket_manager import manager
import logging

logger = logging.getLogger(__name__)

class MQTTClient:
    def __init__(self):
        self.client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2, client_id=settings.mqtt_client_id)
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message
        self.client.on_disconnect = self.on_disconnect
        self.connected = False

    def on_connect(self, client, userdata, connect_flags, reason_code, properties):
        if reason_code == 0:
            logger.info("MQTT connected successfully")
            self.connected = True
            client.subscribe(settings.mqtt_topic)
        else:
            logger.error(f"MQTT connection failed with code {reason_code}")

    def on_disconnect(self, client, userdata, disconnect_flags, reason_code, properties):
        if reason_code != 0:
            logger.warning(f"Unexpected MQTT disconnection: {reason_code}")
        self.connected = False

    def on_message(self, client, userdata, msg):
        try:
            payload = json.loads(msg.payload.decode())
            asyncio.create_task(self.process_message(payload))
        except json.JSONDecodeError:
            logger.error(f"Failed to decode MQTT message: {msg.payload}")
        except Exception as e:
            logger.error(f"Error processing MQTT message: {e}")

    async def process_message(self, payload: dict):
        try:
            # Parse timestamp
            timestamp_str = payload.get("timestamp", datetime.utcnow().isoformat())
            timestamp = datetime.fromisoformat(timestamp_str.replace("Z", "+00:00"))

            # Save to database
            db = SessionLocal()
            location = DeviceLocation(
                device_id=payload.get("device_id"),
                latitude=payload.get("latitude"),
                longitude=payload.get("longitude"),
                battery=payload.get("battery"),
                signal_strength=payload.get("signal_strength"),
                status=payload.get("status", "active"),
                timestamp=timestamp
            )
            db.add(location)
            db.commit()
            db.close()

            # Broadcast to WebSocket clients
            await manager.broadcast_location_update({
                "device_id": payload.get("device_id"),
                "latitude": payload.get("latitude"),
                "longitude": payload.get("longitude"),
                "battery": payload.get("battery"),
                "signal_strength": payload.get("signal_strength"),
                "status": payload.get("status", "active"),
                "timestamp": timestamp.isoformat()
            })

            logger.info(f"Processed location update for device {payload.get('device_id')}")
        except Exception as e:
            logger.error(f"Error processing message: {e}")

    def connect(self):
        try:
            self.client.connect(settings.mqtt_broker, settings.mqtt_port, keepalive=60)
            self.client.loop_start()
            logger.info(f"Connecting to MQTT broker at {settings.mqtt_broker}:{settings.mqtt_port}")
        except Exception as e:
            logger.error(f"Failed to connect to MQTT broker: {e}")

    def disconnect(self):
        self.client.loop_stop()
        self.client.disconnect()

mqtt_client = MQTTClient()
