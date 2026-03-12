from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional

class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str

class UserResponse(BaseModel):
    id: int
    username: str
    email: str
    created_at: datetime

    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Optional[str] = None

class LocationData(BaseModel):
    device_id: str
    latitude: float
    longitude: float
    battery: Optional[int] = None
    signal_strength: Optional[int] = None
    status: str = "active"
    timestamp: datetime

class LocationResponse(LocationData):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True

class WebSocketMessage(BaseModel):
    type: str
    data: LocationData
