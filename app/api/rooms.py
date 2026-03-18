from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.core.database import get_db
from app.core.deps import get_current_active_user, require_role
from app.models.room import Room
from app.models.user import User
from app.schemas.room import RoomCreate, RoomUpdate, RoomResponse

router = APIRouter(prefix="/api/rooms", tags=["Помещения"])


@router.get("/", response_model=List[RoomResponse])
def get_rooms(
        skip: int = 0,
        limit: int = 100,
        db: Session = Depends(get_db)
):
    """
    Получить список всех помещений.

    - **skip**: сколько пропустить (для пагинации)
    - **limit**: сколько вернуть (максимум)
    """
    rooms = db.query(Room).filter(Room.is_active == True).offset(skip).limit(limit).all()
    return rooms


@router.get("/{room_id}", response_model=RoomResponse)
def get_room(
        room_id: int,
        db: Session = Depends(get_db)
):
    """
    Получить детальную информацию о конкретном помещении.
    """
    room = db.query(Room).filter(Room.id == room_id, Room.is_active == True).first()
    if not room:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Помещение не найдено"
        )
    return room


@router.post("/", response_model=RoomResponse, status_code=status.HTTP_201_CREATED)
def create_room(
        room_data: RoomCreate,
        db: Session = Depends(get_db),
        current_user: User = Depends(require_role("admin"))
):
    """
    Создать новое помещение (только для администраторов).
    """
    new_room = Room(
        name=room_data.name,
        description=room_data.description,
        capacity=room_data.capacity,
        equipment=room_data.equipment,
        image_url=room_data.image_url
    )

    db.add(new_room)
    db.commit()
    db.refresh(new_room)

    return new_room


@router.put("/{room_id}", response_model=RoomResponse)
def update_room(
        room_id: int,
        room_data: RoomUpdate,
        db: Session = Depends(get_db),
        current_user: User = Depends(require_role("admin"))
):
    """
    Обновить информацию о помещении (только для администраторов).
    """
    room = db.query(Room).filter(Room.id == room_id).first()
    if not room:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Помещение не найдено"
        )

    # Обновляем только переданные поля
    update_data = room_data.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(room, field, value)

    db.commit()
    db.refresh(room)

    return room


@router.delete("/{room_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_room(
        room_id: int,
        db: Session = Depends(get_db),
        current_user: User = Depends(require_role("admin"))
):
    """
    Удалить помещение (помечать как неактивное, а не удалять физически).
    """
    room = db.query(Room).filter(Room.id == room_id).first()
    if not room:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Помещение не найдено"
        )

    # Soft delete — помечаем как неактивное
    room.is_active = False
    db.commit()

    return None