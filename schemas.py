# schemas.py
from pydantic import BaseModel
from typing import List, Optional

# --- Room Schemas ---
class RoomBase(BaseModel):
    name: str

class RoomCreate(RoomBase):
    pass

class Room(RoomBase):
    id: int
    uuid: str
    owner_id: int

    class Config:
        orm_mode = True # Allows Pydantic to read data from ORM models

# --- User Schemas ---
class UserBase(BaseModel):
    username: str

class UserCreate(UserBase):
    password: str

class User(UserBase):
    id: int
    is_active: bool = True # Assuming all users are active
    rooms: List[Room] = []

    class Config:
        orm_mode = True

# --- Token Schema for Authentication ---
class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Optional[str] = None

