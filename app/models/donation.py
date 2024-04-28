from sqlalchemy import Column, ForeignKey, Integer, Text

from .abstract import BaseAbstractAmount

INFO_ABOUT_DONATION = (
    'ID пользователя: {id}, сообщение от пользователя: {comment:30}. '
    '{info_about_amount}'
)


class Donation(BaseAbstractAmount):
    user_id = Column(Integer, ForeignKey('user.id'))
    comment = Column(Text)

    def __repr__(self) -> str:
        return INFO_ABOUT_DONATION.format(
            user_id=self.user_id,
            comment=self.comment,
            info_about_amont=super().__repr__()
        )
