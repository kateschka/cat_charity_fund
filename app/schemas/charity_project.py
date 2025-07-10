from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field, root_validator, validator

from app.core.error_message import ErrorMessage
from app.schemas.base import PositiveInteger
from .constants import MIN_STRING_LENGTH, MAX_STRING_LENGTH


class CharityProjectBase(BaseModel):
    name: str = Field(..., min_length=MIN_STRING_LENGTH,
                      max_length=MAX_STRING_LENGTH)
    description: str = Field(..., min_length=MIN_STRING_LENGTH)
    full_amount: PositiveInteger


class CharityProjectCreate(CharityProjectBase):
    pass


class CharityProjectUpdate(BaseModel):
    name: Optional[str] = Field(
        None, min_length=MIN_STRING_LENGTH, max_length=MAX_STRING_LENGTH)
    description: Optional[str] = Field(None, min_length=MIN_STRING_LENGTH)
    full_amount: Optional[PositiveInteger] = None

    @validator('full_amount')
    def check_full_amount(cls, v):
        if v is not None and v <= 0:
            raise ValueError(ErrorMessage.INVALID_FULL_AMOUNT)
        return v

    @root_validator
    def check_at_least_one_field(cls, values):
        if all(value is None for value in values.values()):
            raise ValueError(ErrorMessage.REQUEST_EMPTY_BODY)
        return values


class CharityProjectDB(CharityProjectBase):
    id: int
    invested_amount: int
    fully_invested: bool
    create_date: datetime
    close_date: Optional[datetime]

    class Config:
        orm_mode = True
