# crud.py
from sqlalchemy.orm import Session
import models, schemas, security

# --- User CRUD ---
def get_user_by_username(db: Session, username: str):
    return db.query(models.User).filter(models.User.username == username).first()

def create_user(db: Session, user: schemas.UserCreate):
    hashed_password = security.get_password_hash(user.password)
    db_user = models.User(username=user.username, hashed_password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

# --- Room CRUD ---
def get_rooms_by_user(db: Session, user_id: int):
    return db.query(models.Room).filter(models.Room.owner_id == user_id).all()

def create_user_room(db: Session, room: schemas.RoomCreate, user_id: int, room_uuid: str):
    db_room = models.Room(**room.dict(), owner_id=user_id, uuid=room_uuid)
    db.add(db_room)
    db.commit()
    db.refresh(db_room)
    return db_room

def get_room_by_uuid(db: Session, room_uuid: str):
    return db.query(models.Room).filter(models.Room.uuid == room_uuid).first()

