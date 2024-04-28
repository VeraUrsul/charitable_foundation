from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Extra, Field, PositiveInt

EXAMPLE_FULL_AMOUNT = 1000
HELPING_FAMILIES = 'Поможем семьям потерявшим дома из-за паводка'
MAX_LENGTH_NAME = 100
MIX_LENGTH_NAME = 1
NEW_HOUSING = 'Новое жильё'


class CharityProjectUpdate(BaseModel):
    name: Optional[str] = Field(None, max_length=MAX_LENGTH_NAME)
    description: Optional[str]
    full_amount: Optional[PositiveInt]

    class Config:
        extra = Extra.forbid
        min_anystr_length = MIX_LENGTH_NAME
        schema_extra = dict(
            example=dict(
                name=NEW_HOUSING,
                description=HELPING_FAMILIES,
                full_amount=EXAMPLE_FULL_AMOUNT
            )
        )


class CharityProjectCreate(CharityProjectUpdate):
    name: str = Field(..., max_length=MAX_LENGTH_NAME)
    description: str
    full_amount: PositiveInt


class CharityProjectDB(CharityProjectCreate):
    id: int
    invested_amount: int
    fully_invested: bool = Field(False)
    create_date: datetime
    close_date: Optional[datetime]

    class Config:
        orm_mode = True
