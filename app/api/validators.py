from http import HTTPStatus

from fastapi import HTTPException
from pydantic import PositiveInt
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud import charity_project_crud
from app.models import CharityProject

SMALL_FULL_AMOUNT = 'Сумма должна быть больше {invested_amount}!'
NAME_IS_TAKEN = 'Проект с таким именем уже существует!'
PROJECT_DOES_NOT_EXIST = 'Проект не существует!'
PROJECT_IS_CLOSED = 'Закрытый проект нельзя редактировать!'
PROJECT_WITH_DONATION = 'В проект были внесены средства, не подлежит удалению!'


async def check_name_duplicate(
    project_name: str,
    session: AsyncSession,
) -> None:
    """Проверка имени на уникальность."""
    project_id = await charity_project_crud.get_project_id_by_name(
        project_name, session
    )
    if project_id:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail=NAME_IS_TAKEN,
        )


async def check_charity_project_exists(
    project_id: int,
    session: AsyncSession,
) -> CharityProject:
    """Проверка наличия объекта в базе данных."""
    project = await charity_project_crud.get(project_id, session)
    if project is None:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail=PROJECT_DOES_NOT_EXIST
        )
    return project


async def check_full_amount_for_update(
    project_id: int,
    session: AsyncSession,
    new_full_amount: PositiveInt
) -> None:
    """Проверка требуемой суммы при обновлении объекта."""
    project = await check_charity_project_exists(project_id, session)
    if project.fully_invested:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail=PROJECT_IS_CLOSED
        )
    if new_full_amount and new_full_amount < project.invested_amount:
        raise HTTPException(
            status_code=HTTPStatus.UNPROCESSABLE_ENTITY,
            detail=SMALL_FULL_AMOUNT.format(
                invested_amount=project.invested_amount
            )
        )


async def check_project_is_not_invested(
    project_id: int,
    session: AsyncSession,
) -> None:
    """Проверка отсутствия инвестиций в проекте."""
    project = await check_charity_project_exists(project_id, session)
    if project.invested_amount:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail=PROJECT_WITH_DONATION
        )


async def check_project_is_not_closed(
    project_id: int,
    session: AsyncSession,
) -> None:
    """Проверка, что проект закрыт."""
    project = await check_charity_project_exists(project_id, session)
    if project.fully_invested:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail=PROJECT_WITH_DONATION
        )
