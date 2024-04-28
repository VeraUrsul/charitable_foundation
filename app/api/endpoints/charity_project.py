from fastapi import APIRouter, Depends

from sqlalchemy.ext.asyncio import AsyncSession

from app.api.validators import (
    check_charity_project_exists, check_full_amount_for_update,
    check_name_duplicate, check_project_is_not_closed,
    check_project_is_not_invested
)
from app.core.db import get_async_session
from app.core.user import current_superuser
from app.crud import charity_project_crud, donation_crud
from app.schemas import (
    CharityProjectCreate, CharityProjectDB, CharityProjectUpdate
)
from app.services import investment_process

router = APIRouter()

DELETE_PROJECT = 'Удалить проект'
LIST_OF_ALL_PROJECTS = 'Получить список всех проектов'
MAIN_PATH = '/'
MAKE_NEW_DONATION_PROJECT = 'Создать новый проект для пожертвований'
PROJECT_ID_PATH = '/{project_id}'
UPDATE_PROJECT = 'Обновить проект'


@router.post(
    MAIN_PATH,
    summary=MAKE_NEW_DONATION_PROJECT,
    response_model=CharityProjectDB,
    response_model_exclude_none=True,
    dependencies=[Depends(current_superuser)],
)
async def create_new_charity_project(
    project: CharityProjectCreate,
    session: AsyncSession = Depends(get_async_session),
):
    """Только для суперюзеров."""
    await check_name_duplicate(project.name, session)
    new_project = await charity_project_crud.create(
        project, session, need_commit=False
    )
    session.add_all(
        investment_process(
            new_project,
            await donation_crud.get_not_fully_invested_object(session)
        )
    )
    await session.commit()
    await session.refresh(new_project)
    return new_project


@router.get(
    MAIN_PATH,
    summary=LIST_OF_ALL_PROJECTS,
    response_model=list[CharityProjectDB],
    response_model_exclude_none=True,
)
async def get_all_charity_project(
    session: AsyncSession = Depends(get_async_session),
):
    return await charity_project_crud.get_multi(session)


@router.patch(
    PROJECT_ID_PATH,
    summary=UPDATE_PROJECT,
    response_model=CharityProjectDB,
    dependencies=[Depends(current_superuser)],
)
async def partially_update_charity_project(
    project_id: int,
    obj_in: CharityProjectUpdate,
    session: AsyncSession = Depends(get_async_session),
):
    """Только для суперюзеров."""
    project = await check_charity_project_exists(project_id, session)
    if obj_in.name:
        await check_name_duplicate(obj_in.name, session)
    if obj_in.full_amount:
        await check_full_amount_for_update(
            project_id, session, obj_in.full_amount
        )
    return await charity_project_crud.update(project, obj_in, session)


@router.delete(
    PROJECT_ID_PATH,
    summary=DELETE_PROJECT,
    response_model=CharityProjectDB,
    dependencies=[Depends(current_superuser)],
)
async def remove_charity_project(
    project_id: int,
    session: AsyncSession = Depends(get_async_session),
):
    """Только для суперюзеров."""
    project = await check_charity_project_exists(project_id, session)
    await check_project_is_not_closed(project_id, session)
    await check_project_is_not_invested(project_id, session)
    return await charity_project_crud.remove(project, session)
