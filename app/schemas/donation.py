from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Extra, PositiveInt

COMMENT_CAT = 'Чтобы кисам хорошо жилось!'
FULL_AMOUNT = 200


class DonationCreate(BaseModel):
    """Схема создания пожертвования."""
    full_amount: PositiveInt
    comment: Optional[str]

    class Config:
        extra = Extra.forbid
        schema_extra = dict(
            example=dict(
                full_amoun=FULL_AMOUNT,
                comment=COMMENT_CAT
            )
        )


class DonationResponse(DonationCreate):
    """Схема создания пожертвования."""
    id: int
    create_date: datetime

    class Config:
        orm_mode = True


class DonationDB(DonationResponse):
    """Схема для отображения всех данных объекта пожертвования"""
    user_id: Optional[int]
    invested_amount: Optional[int]
    fully_invested: Optional[bool]
    close_date: Optional[datetime]
