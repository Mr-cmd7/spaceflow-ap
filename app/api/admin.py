from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime

from app.core.database import get_db
from app.core.deps import require_role
from app.models.booking import Booking
from app.models.user import User
from app.schemas.booking import AdminBookingResponse

router = APIRouter(prefix="/api/admin", tags=["Администрирование"])


@router.get("/bookings", response_model=List[AdminBookingResponse])
def get_all_bookings(
        status_filter: Optional[str] = None,
        room_id: Optional[int] = None,
        db: Session = Depends(get_db),
        admin: User = Depends(require_role("admin"))
):
    """
    Получение всех бронирований с информацией о пользователе и помещении.
    Только для администраторов.
    """
    query = db.query(Booking)

    if status_filter:
        query = query.filter(Booking.status == status_filter)

    if room_id:
        query = query.filter(Booking.room_id == room_id)

    # Загружаем связанные объекты user и room (они уже есть в модели через relationship)
    bookings = query.order_by(Booking.start_time.desc()).all()
    return bookings


@router.put("/bookings/{booking_id}/confirm", response_model=AdminBookingResponse)
def confirm_booking(
        booking_id: int,
        db: Session = Depends(get_db),
        admin: User = Depends(require_role("admin"))
):
    booking = db.query(Booking).filter(Booking.id == booking_id).first()

    if not booking:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Бронирование не найдено"
        )

    if booking.status != "pending":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Нельзя подтвердить бронирование со статусом {booking.status}"
        )

    booking.status = "confirmed"
    db.commit()
    db.refresh(booking)
    return booking


@router.put("/bookings/{booking_id}/reject", response_model=AdminBookingResponse)
def reject_booking(
        booking_id: int,
        db: Session = Depends(get_db),
        admin: User = Depends(require_role("admin"))
):
    booking = db.query(Booking).filter(Booking.id == booking_id).first()

    if not booking:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Бронирование не найдено"
        )

    if booking.status != "pending":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Нельзя отклонить бронирование со статусом {booking.status}"
        )

    booking.status = "rejected"
    db.commit()
    db.refresh(booking)
    return booking