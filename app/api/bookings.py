from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime, timezone

from app.core.database import get_db
from app.core.deps import get_current_active_user
from app.models.booking import Booking
from app.models.room import Room
from app.models.user import User
from app.schemas.booking import BookingCreate, BookingResponse, BookingListItem

router = APIRouter(prefix="/api/bookings", tags=["Бронирования"])


@router.post("/", response_model=BookingResponse, status_code=status.HTTP_201_CREATED)
def create_booking(
        booking_data: BookingCreate,
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_active_user)
):
    room = db.query(Room).filter(
        Room.id == booking_data.room_id,
        Room.is_active == True
    ).first()

    if not room:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Помещение не найдено"
        )

    existing_booking = db.query(Booking).filter(
        Booking.room_id == booking_data.room_id,
        Booking.status.in_(["pending", "confirmed"]),
        Booking.start_time < booking_data.end_time,
        Booking.end_time > booking_data.start_time
    ).first()

    if existing_booking:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Это время уже занято"
        )

    new_booking = Booking(
        user_id=current_user.id,
        room_id=booking_data.room_id,
        start_time=booking_data.start_time,
        end_time=booking_data.end_time,
        purpose=booking_data.purpose,
        participants_count=booking_data.participants_count,
        status="pending"
    )

    db.add(new_booking)
    db.commit()
    db.refresh(new_booking)

    return new_booking


@router.get("/my", response_model=List[BookingListItem])
def get_my_bookings(
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_active_user)
):
    bookings = db.query(Booking).filter(
        Booking.user_id == current_user.id
    ).order_by(Booking.start_time.desc()).all()

    result = []
    for booking in bookings:
        result.append({
            "id": booking.id,
            "room_name": booking.room.name,
            "start_time": booking.start_time,
            "end_time": booking.end_time,
            "status": booking.status
        })

    return result


@router.put("/{booking_id}/cancel", response_model=BookingResponse)
def cancel_booking(
        booking_id: int,
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_active_user)
):
    booking = db.query(Booking).filter(Booking.id == booking_id).first()

    if not booking:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Бронирование не найдено"
        )

    if booking.user_id != current_user.id and current_user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Нельзя отменить чужое бронирование"
        )

    # Исправлено: используем timezone.utc для сравнения с aware datetime
    if booking.start_time < datetime.now(timezone.utc):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Нельзя отменить уже начавшееся бронирование"
        )

    if booking.status in ["cancelled", "completed", "rejected"]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Бронирование уже {booking.status}"
        )

    booking.status = "cancelled"
    db.commit()
    db.refresh(booking)

    return booking