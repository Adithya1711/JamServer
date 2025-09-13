# routers/rooms.py
import os
import uuid
from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
import crud, schemas
from database import get_db
from dependencies import get_current_active_user

router = APIRouter(prefix="/rooms", dependencies=[Depends(get_current_active_user)])

# --- Create Room Endpoint ---
@router.post("/", response_model=schemas.Room, status_code=201)
def create_room(
    room: schemas.RoomCreate,
    db: Session = Depends(get_db),
    current_user: schemas.User = Depends(get_current_active_user),
):
    room_uuid = str(uuid.uuid4())
    room_path = os.path.join("uploads", room_uuid)
    os.makedirs(room_path, exist_ok=True)
    return crud.create_user_room(db=db, room=room, user_id=current_user.id, room_uuid=room_uuid)


# --- List Rooms Endpoint ---
@router.get("/", response_model=List[schemas.Room])
def read_rooms(
    db: Session = Depends(get_db),
    current_user: schemas.User = Depends(get_current_active_user),
):
    rooms = crud.get_rooms_by_user(db, user_id=current_user.id)
    return rooms

