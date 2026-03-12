# Quick Start Guide

## 1. Start MQTT Broker (Local Testing)

**Windows (WSL):**
```bash
# Install mosquitto in WSL
sudo apt-get install mosquitto

# Start mosquitto
mosquitto -v
```

**macOS:**
```bash
brew install mosquitto
mosquitto -v
```

**Linux:**
```bash
sudo apt-get install mosquitto
mosquitto -v
```

## 2. Start Backend Server

```bash
cd backend
pip install -r requirements.txt
python main.py
```

Expected output:
```
INFO:     Uvicorn running on http://0.0.0.0:8000
```

## 3. Start Frontend Development Server

In a new terminal:
```bash
cd frontend
npm install
npm run dev
```

Expected output:
```
  VITE v5.0.8  ready in 123 ms

  ➜  Local:   http://localhost:5173/
```

## 4. Test with Sample Data

In another terminal:
```bash
cd backend
python test_mqtt.py
```

This will publish test location data from 3 simulated devices.

## 5. View the Application

Open your browser and go to: `http://localhost:5173`

You should see:
- A map with device markers
- A device panel on the left showing device information
- Real-time updates as new MQTT messages arrive

## Testing MQTT Manually

To publish a test message manually:

```bash
mosquitto_pub -h localhost -p 1883 -t "devices/location/device_001" -m '{
  "device_id": "device_001",
  "latitude": 39.9042,
  "longitude": 116.4074,
  "battery": 85,
  "signal_strength": -65,
  "status": "active",
  "timestamp": "2026-03-12T10:30:00Z"
}'
```

## API Testing

Check backend health:
```bash
curl http://localhost:8000/health
```

Get all device locations:
```bash
curl http://localhost:8000/devices
```

Get device history (last 24 hours):
```bash
curl http://localhost:8000/devices/device_001/history
```

## Troubleshooting

**Backend won't start:**
- Check if port 8000 is already in use
- Verify Python 3.8+ is installed
- Check requirements.txt installation

**Frontend won't start:**
- Check if port 5173 is already in use
- Verify Node.js 16+ is installed
- Run `npm install` again

**No devices on map:**
- Verify MQTT broker is running
- Check backend logs for MQTT connection
- Run `python test_mqtt.py` to send test data
- Check browser console for errors

**WebSocket connection failed:**
- Ensure backend is running
- Check browser console for connection errors
- Verify firewall allows WebSocket connections
