from datetime import datetime

from sqlalchemy import Boolean, CheckConstraint, Column, DateTime, Integer

from app.core.db import Base

INFO_ABOUT_AMOUNT = (
    'Сумма: {full_amount}, из которой уже задействовано: {invested_amount}, '
    'дата открытия: {create_date}, дата закрытия: {close_date}. '
)


class BaseAbstractAmount(Base):
    __abstract__ = True
    __table_args__ = (
        CheckConstraint('0 < full_amount'),
        CheckConstraint('invested_amount <= full_amount')
    )
    full_amount = Column(Integer, nullable=False)
    invested_amount = Column(Integer, nullable=False, default=0)
    fully_invested = Column(Boolean, default=False)
    create_date = Column(DateTime, default=datetime.now)
    close_date = Column(DateTime, default=None)

    def __repr__(self) -> str:
        return INFO_ABOUT_AMOUNT.format(
            full_amount=self.full_amount,
            invested_amount=self.invested_amount,
            create_date=self.create_date,
            close_date=self.close_date
        )
