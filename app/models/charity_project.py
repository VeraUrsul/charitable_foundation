from sqlalchemy import Column, String, Text

from .abstract import BaseAbstractAmount

INFO_ABOUT_PROJECT = (
    'Проект: {name:30}, описание: {description:30} {info_about_amont}')
MAX_LENGHT_OF_PROJECT_NAME = 100


class CharityProject(BaseAbstractAmount):
    name = Column(
        String(MAX_LENGHT_OF_PROJECT_NAME), unique=True, nullable=False
    )
    description = Column(Text)

    def __repr__(self) -> str:
        return INFO_ABOUT_PROJECT.format(
            name=self.name,
            description=self.description,
            info_about_amont=super().__repr__()
        )
