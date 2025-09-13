# routers/upload.py
import os
import shutil
from fastapi import APIRouter, Depends, HTTPException, File, UploadFile, status
from sqlalchemy.orm import Session
import crud, schemas
from database import get_db
from dependencies import get_current_active_user

router = APIRouter(prefix="/upload", dependencies=[Depends(get_current_active_user)])

@router.post("/{room_uuid}")
async def upload_file(
    room_uuid: str,
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: schemas.User = Depends(get_current_active_user),
):
    # 1. Verify the room exists and the user owns it
    room = crud.get_room_by_uuid(db, room_uuid=room_uuid)
    if not room:
        raise HTTPException(status_code=404, detail="Room not found")
    if room.owner_id != current_user.id: # type: ignore
        raise HTTPException(status_code=403, detail="Not authorized to upload to this room")

    # 2. Define the file path and save the file
    upload_folder = os.path.join("uploads", room_uuid)
    file_path = os.path.join(upload_folder, file.filename) # type: ignore

    try:
        # Save the uploaded file by streaming its contents to a new file.
        # This is memory-efficient for large files.
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Could not save file: {e}")
    finally:
        file.file.close() # Ensure the file is closed

    return {
        "message": f"Successfully uploaded {file.filename} to room {room.name}",
        "filename": file.filename,
    }

