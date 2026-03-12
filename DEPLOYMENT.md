# Deployment Guide

## Docker Compose (Recommended for Local/Development)

### Prerequisites
- Docker and Docker Compose installed

### Quick Start

```bash
docker-compose up -d
```

This will start:
- MQTT Broker (mosquitto) on port 1883
- Backend API on port 8000
- Frontend on port 5173

Access the application at: `http://localhost:5173`

### Stop Services

```bash
docker-compose down
```

### View Logs

```bash
docker-compose logs -f backend
docker-compose logs -f frontend
docker-compose logs -f mosquitto
```

## Production Deployment

### 1. Backend Deployment (AWS EC2 / DigitalOcean)

**Using Gunicorn + Nginx:**

```bash
# Install dependencies
pip install -r requirements.txt
pip install gunicorn

# Run with Gunicorn
gunicorn -w 4 -b 0.0.0.0:8000 main:app
```

**Nginx Configuration:**

```nginx
server {
    listen 80;
    server_name your-domain.com;

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

### 2. Frontend Deployment

**Build for Production:**

```bash
cd frontend
npm run build
```

**Serve with Nginx:**

```nginx
server {
    listen 80;
    server_name your-domain.com;
    root /var/www/location-tracking/dist;

    location / {
        try_files $uri $uri/ /index.html;
    }

    location /api {
        proxy_pass http://backend-server:8000;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
    }
}
```

### 3. MQTT Broker (Production)

**Option A: Self-Hosted Mosquitto**

```bash
docker run -d \
  --name mosquitto \
  -p 1883:1883 \
  -p 9001:9001 \
  -v mosquitto_data:/mosquitto/data \
  eclipse-mosquitto
```

**Option B: Cloud MQTT Services**
- AWS IoT Core
- Azure IoT Hub
- Google Cloud IoT
- HiveMQ Cloud

Update `MQTT_BROKER` in `.env` to your cloud service endpoint.

### 4. Database (Production)

**Switch from SQLite to PostgreSQL:**

1. Install PostgreSQL
2. Update `DATABASE_URL` in `.env`:
   ```
   DATABASE_URL=postgresql://user:password@localhost/location_db
   ```

3. Install psycopg2:
   ```bash
   pip install psycopg2-binary
   ```

4. Update `database.py` to use PostgreSQL connection string

### 5. SSL/TLS Certificates

**Using Let's Encrypt with Certbot:**

```bash
sudo apt-get install certbot python3-certbot-nginx
sudo certbot certonly --nginx -d your-domain.com
```

**Update Nginx:**

```nginx
server {
    listen 443 ssl http2;
    server_name your-domain.com;

    ssl_certificate /etc/letsencrypt/live/your-domain.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/your-domain.com/privkey.pem;

    # ... rest of configuration
}

# Redirect HTTP to HTTPS
server {
    listen 80;
    server_name your-domain.com;
    return 301 https://$server_name$request_uri;
}
```

### 6. Environment Variables

Create `.env` file with production values:

```env
MQTT_BROKER=your-mqtt-broker.com
MQTT_PORT=8883
MQTT_TOPIC=devices/location/#
DATABASE_URL=postgresql://user:password@db-host/location_db
SERVER_HOST=0.0.0.0
SERVER_PORT=8000
```

### 7. Monitoring & Logging

**Application Logging:**

```python
# In main.py
import logging
from pythonjsonlogger import jsonlogger

logHandler = logging.StreamHandler()
formatter = jsonlogger.JsonFormatter()
logHandler.setFormatter(formatter)
logger = logging.getLogger()
logger.addHandler(logHandler)
logger.setLevel(logging.INFO)
```

**System Monitoring:**
- Use PM2 for process management
- Set up Prometheus + Grafana for metrics
- Configure ELK stack for log aggregation

### 8. Systemd Service (Linux)

Create `/etc/systemd/system/location-tracking.service`:

```ini
[Unit]
Description=Location Tracking Backend
After=network.target

[Service]
Type=notify
User=www-data
WorkingDirectory=/opt/location-tracking/backend
ExecStart=/usr/bin/python3 /opt/location-tracking/backend/main.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

Enable and start:

```bash
sudo systemctl enable location-tracking
sudo systemctl start location-tracking
```

### 9. Backup Strategy

**Database Backups:**

```bash
# PostgreSQL backup
pg_dump location_db > backup_$(date +%Y%m%d).sql

# Restore
psql location_db < backup_20260312.sql
```

**Automated Backups (Cron):**

```bash
0 2 * * * pg_dump location_db | gzip > /backups/location_db_$(date +\%Y\%m\%d).sql.gz
```

## Scaling Considerations

1. **Load Balancing**: Use Nginx or HAProxy to distribute traffic
2. **Database Replication**: Set up PostgreSQL replication for HA
3. **Message Queue**: Consider Redis for caching device locations
4. **CDN**: Serve frontend assets from CDN
5. **Horizontal Scaling**: Run multiple backend instances behind load balancer

## Security Checklist

- [ ] Enable HTTPS/TLS
- [ ] Set up firewall rules
- [ ] Use strong database passwords
- [ ] Enable MQTT authentication
- [ ] Implement API rate limiting
- [ ] Add request validation
- [ ] Set up CORS properly
- [ ] Use environment variables for secrets
- [ ] Enable database encryption
- [ ] Set up regular backups
- [ ] Monitor for suspicious activity
- [ ] Keep dependencies updated
