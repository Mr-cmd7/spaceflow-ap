from pydantic import BaseModel, Field, validator
from typing import Optional
from datetime import datetime


class BookingBase(BaseModel):
    room_id: int
    start_time: datetime
    end_time: datetime
    purpose: Optional[str] = None
    participants_count: Optional[int] = Field(None, gt=0, le=1000)


class BookingCreate(BookingBase):
    @validator('end_time')
    def validate_end_time(cls, v, values):
        """Проверяет, что end_time позже start_time"""
        if 'start_time' in values and v <= values['start_time']:
            raise ValueError('end_time должно быть позже start_time')
        return v

    @validator('start_time')
    def validate_start_time(cls, v):
        """Проверяет, что start_time не в прошлом"""
        if v < datetime.now():
            raise ValueError('start_time не может быть в прошлом')
        return v


class BookingResponse(BaseModel):
    id: int
    user_id: int
    room_id: int
    start_time: datetime
    end_time: datetime
    status: str
    purpose: Optional[str]
    participants_count: Optional[int]
    created_at: datetime

    class Config:
        from_attributes = True


# Для списка бронирований с краткой информацией
class BookingListItem(BaseModel):
    id: int
    room_name: str
    start_time: datetime
    end_time: datetime
    status: str

    class Config:
        from_attributes = True


class UserBrief(BaseModel):
    """Краткая информация о пользователе для админ-панели"""
    email: str
    full_name: str

    class Config:
        from_attributes = True


class RoomBrief(BaseModel):
    """Краткая информация о помещении для админ-панели"""
    name: str

    class Config:
        from_attributes = True


class AdminBookingResponse(BookingResponse):
    """Расширенный ответ для админ-панели, включающий данные пользователя и помещения"""
    user: UserBrief
    room: RoomBrief

    class Config:
        from_attributes = True