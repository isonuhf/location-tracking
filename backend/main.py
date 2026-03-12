from fastapi import FastAPI, WebSocket, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
import logging

from config import settings
from database import get_db, DeviceLocation, User
from models import LocationResponse, UserCreate, UserResponse, Token
from mqtt_client import mqtt_client
from websocket_manager import manager
from auth import (
    get_current_user,
    create_access_token,
    get_password_hash,
    verify_password
)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="Location Tracking System")

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
async def startup_event():
    logger.info("Starting up application")
    mqtt_client.connect()

@app.on_event("shutdown")
async def shutdown_event():
    logger.info("Shutting down application")
    mqtt_client.disconnect()

@app.post("/auth/register", response_model=UserResponse)
async def register(user: UserCreate, db: Session = Depends(get_db)):
    """Register a new user"""
    db_user = db.query(User).filter(User.username == user.username).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Username already registered")

    db_user = db.query(User).filter(User.email == user.email).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    hashed_password = get_password_hash(user.password)
    db_user = User(username=user.username, email=user.email, hashed_password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

@app.post("/auth/login", response_model=Token)
async def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    """Login user and return JWT token"""
    user = db.query(User).filter(User.username == form_data.username).first()
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token_expires = timedelta(minutes=settings.access_token_expire_minutes)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

@app.get("/auth/me", response_model=UserResponse)
async def get_me(current_user: User = Depends(get_current_user)):
    """Get current user info"""
    return current_user

@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "mqtt_connected": mqtt_client.connected,
        "timestamp": datetime.utcnow().isoformat()
    }

@app.get("/devices", response_model=list[LocationResponse])
async def get_latest_devices(db: Session = Depends(get_db)):
    """Get latest location for each device"""
    subquery = db.query(
        DeviceLocation.device_id,
        DeviceLocation.id
    ).distinct(DeviceLocation.device_id).order_by(
        DeviceLocation.device_id,
        DeviceLocation.timestamp.desc()
    ).subquery()

    locations = db.query(DeviceLocation).filter(
        DeviceLocation.id.in_(
            db.query(subquery.c.id)
        )
    ).all()

    return locations

@app.get("/devices/{device_id}/history", response_model=list[LocationResponse])
async def get_device_history(
    device_id: str,
    hours: int = 24,
    db: Session = Depends(get_db)
):
    """Get location history for a specific device"""
    cutoff_time = datetime.utcnow() - timedelta(hours=hours)
    locations = db.query(DeviceLocation).filter(
        DeviceLocation.device_id == device_id,
        DeviceLocation.timestamp >= cutoff_time
    ).order_by(DeviceLocation.timestamp.desc()).all()

    if not locations:
        raise HTTPException(status_code=404, detail="Device not found")

    return locations

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_text()
    except Exception as e:
        logger.error(f"WebSocket error: {e}")
    finally:
        manager.disconnect(websocket)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host=settings.server_host, port=settings.server_port)
