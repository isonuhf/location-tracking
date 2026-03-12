# Smart Hardware Location Tracking System

A real-time location tracking system for IoT devices using MQTT, FastAPI, and Vue 3.

## System Architecture

```
IoT Devices (MQTT) → MQTT Broker → FastAPI Backend → WebSocket → Vue 3 Frontend (Leaflet Map)
```

## Prerequisites

- Python 3.8+
- Node.js 16+
- MQTT Broker (mosquitto or cloud-based)

## Backend Setup

### 1. Install Dependencies

```bash
cd backend
pip install -r requirements.txt
```

### 2. Configure MQTT Broker

Edit `.env` to set your MQTT broker details:

```env
MQTT_BROKER=localhost
MQTT_PORT=1883
MQTT_TOPIC=devices/location/#
```

For local testing, install and run mosquitto:

**Windows (using WSL or native):**
```bash
# Using WSL
sudo apt-get install mosquitto mosquitto-clients

# Start mosquitto
mosquitto -v
```

**macOS:**
```bash
brew install mosquitto
brew services start mosquitto
```

**Linux:**
```bash
sudo apt-get install mosquitto mosquitto-clients
sudo systemctl start mosquitto
```

### 3. Run Backend Server

```bash
cd backend
python main.py
```

The server will start at `http://localhost:8000`

### 4. Test with MQTT Messages

In another terminal:

```bash
cd backend
python test_mqtt.py
```

This will publish test location data from simulated devices.

## Frontend Setup

### 1. Install Dependencies

```bash
cd frontend
npm install
```

### 2. Run Development Server

```bash
npm run dev
```

The frontend will be available at `http://localhost:5173`

### 3. Build for Production

```bash
npm run build
```

## API Endpoints

### Health Check
```
GET /health
```

### Get Latest Device Locations
```
GET /devices
```

Response:
```json
[
  {
    "id": 1,
    "device_id": "device_001",
    "latitude": 39.9042,
    "longitude": 116.4074,
    "battery": 85,
    "signal_strength": -65,
    "status": "active",
    "timestamp": "2026-03-12T10:30:00",
    "created_at": "2026-03-12T10:30:00"
  }
]
```

### Get Device History
```
GET /devices/{device_id}/history?hours=24
```

## MQTT Message Format

Devices should publish to `devices/location/{device_id}` with this JSON payload:

```json
{
  "device_id": "device_001",
  "latitude": 39.9042,
  "longitude": 116.4074,
  "battery": 85,
  "signal_strength": -65,
  "status": "active",
  "timestamp": "2026-03-12T10:30:00Z"
}
```

## WebSocket Events

The frontend connects to `ws://localhost:8000/ws` and receives:

```json
{
  "type": "location_update",
  "data": {
    "device_id": "device_001",
    "latitude": 39.9042,
    "longitude": 116.4074,
    "battery": 85,
    "signal_strength": -65,
    "status": "active",
    "timestamp": "2026-03-12T10:30:00Z"
  }
}
```

## Features

- ✅ Real-time device location tracking via MQTT
- ✅ WebSocket-based live updates to frontend
- ✅ Interactive Leaflet map with device markers
- ✅ Device information panel with battery and signal strength
- ✅ Location history API
- ✅ Automatic reconnection on connection loss
- ✅ SQLite database for data persistence

## Project Structure

```
.
├── backend/
│   ├── main.py              # FastAPI application
│   ├── mqtt_client.py       # MQTT connection and message handling
│   ├── websocket_manager.py # WebSocket connection management
│   ├── database.py          # Database models and configuration
│   ├── models.py            # Pydantic data models
│   ├── config.py            # Configuration settings
│   ├── requirements.txt     # Python dependencies
│   ├── .env                 # Environment variables
│   └── test_mqtt.py         # MQTT test script
│
└── frontend/
    ├── src/
    │   ├── components/
    │   │   ├── MapView.vue      # Leaflet map component
    │   │   └── DevicePanel.vue  # Device list panel
    │   ├── services/
    │   │   └── websocket.js     # WebSocket client
    │   ├── stores/
    │   │   └── deviceStore.js   # Pinia state management
    │   ├── App.vue              # Root component
    │   └── main.js              # Entry point
    ├── index.html               # HTML template
    ├── vite.config.js           # Vite configuration
    └── package.json             # Node dependencies
```

## Troubleshooting

### MQTT Connection Failed
- Ensure mosquitto is running: `mosquitto -v`
- Check MQTT_BROKER and MQTT_PORT in `.env`
- Verify firewall allows port 1883

### WebSocket Connection Failed
- Ensure backend is running on port 8000
- Check browser console for connection errors
- Verify CORS is enabled (it is by default)

### No Devices Appearing on Map
- Check backend logs for MQTT message processing
- Verify test script is running: `python test_mqtt.py`
- Check browser console for JavaScript errors

## Production Deployment

For production, consider:

1. **MQTT Broker**: Use managed service (AWS IoT Core, Azure IoT Hub, etc.)
2. **Backend**: Deploy with Docker, use PostgreSQL instead of SQLite
3. **Frontend**: Build and serve static files with Nginx
4. **SSL/TLS**: Enable HTTPS and WSS for secure connections
5. **Authentication**: Add API key or JWT authentication
6. **Monitoring**: Set up logging and alerting

## License

MIT
