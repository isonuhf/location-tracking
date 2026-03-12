from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    # MQTT Configuration
    mqtt_broker: str = "localhost"
    mqtt_port: int = 1883
    mqtt_topic: str = "devices/location/#"
    mqtt_client_id: str = "location_server"

    # Database Configuration
    database_url: str = "sqlite:///./location_data.db"

    # Server Configuration
    server_host: str = "0.0.0.0"
    server_port: int = 8000

    # WebSocket Configuration
    ws_heartbeat_interval: int = 30

    # Authentication Configuration
    secret_key: str = "your-secret-key-change-in-production"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30

    class Config:
        env_file = ".env"

settings = Settings()
