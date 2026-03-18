from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class RoomBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    description: Optional[str] = None
    capacity: int = Field(..., gt=0, le=1000)  # gt = greater than, le = less or equal
    equipment: Optional[str] = None
    image_url: Optional[str] = None


class RoomCreate(RoomBase):
    pass


class RoomUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    description: Optional[str] = None
    capacity: Optional[int] = Field(None, gt=0, le=1000)
    equipment: Optional[str] = None
    image_url: Optional[str] = None
    is_active: Optional[bool] = None


class RoomResponse(RoomBase):
    id: int
    is_active: bool
    created_at: datetime

    class Config:
        from_attributes = True