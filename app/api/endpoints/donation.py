from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_async_session
from app.core.user import current_superuser, current_user
from app.crud import charity_project_crud, donation_crud
from app.models.user import User
from app.schemas.donation import DonationCreate, DonationDB, DonationResponse
from app.services.investing import investment_process

router = APIRouter()

LIST_OF_ALL_DONATIONS = 'Получить список всех пожертвований'
LIST_OF_USER_DONATIONS = 'Получить список всех пожертвований пользователя'
MAIN_PATH = '/'
MAKE_DONATION = 'Сделать пожертвование'
USER_PATH = '/my'


@router.get(
    MAIN_PATH,
    summary=LIST_OF_ALL_DONATIONS,
    response_model_exclude_none=True,
    response_model=List[DonationDB],
    dependencies=[Depends(current_superuser)],
)
async def get_all_donations_for_superuser(
    session: AsyncSession = Depends(get_async_session),
):
    """Только для суперпользователей.
    Показывает список всех пожертвований."""
    return await donation_crud.get_multi(session)


@router.get(
    USER_PATH,
    summary=LIST_OF_USER_DONATIONS,
    response_model=List[DonationResponse],
    response_model_exclude_none=True,
    dependencies=[Depends(current_user)],
)
async def get_donations_for_current_user(
    user: User = Depends(current_user),
    session: AsyncSession = Depends(get_async_session),
):
    """Показывает список всех пожертвований пользователя."""
    return await donation_crud.get_by_user(user, session)


@router.post(
    MAIN_PATH,
    summary=MAKE_DONATION,
    response_model_exclude_none=True,
    response_model=DonationResponse,
    dependencies=[Depends(current_user)],
)
async def create_donation(
    donation: DonationCreate,
    session: AsyncSession = Depends(get_async_session),
    user: User = Depends(current_user),
):
    """Делает пожертвование."""
    new_donation = await donation_crud.create(
        donation, session, user, need_commit=False
    )
    session.add_all(
        investment_process(
            new_donation,
            await charity_project_crud.get_not_fully_invested_object(session)
        )
    )
    await session.commit()
    await session.refresh(new_donation)
    return new_donation
