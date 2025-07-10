from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field

from app.schemas.base import PositiveInteger


class DonationBase(BaseModel):
    full_amount: PositiveInteger
    comment: Optional[str] = Field(None, min_length=1)


class DonationCreate(DonationBase):
    pass


class UserDonation(DonationBase):
    id: int
    create_date: datetime

    class Config:
        orm_mode = True


class DonationDB(DonationBase):
    id: int
    user_id: int
    invested_amount: int
    fully_invested: bool
    create_date: datetime
    close_date: Optional[datetime]

    class Config:
        orm_mode = True