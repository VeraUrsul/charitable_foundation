from http import HTTPStatus

from fastapi import APIRouter, HTTPException

from app.core.user import auth_backend, fastapi_users
from app.schemas.user import UserCreate, UserRead, UserUpdate

AUTHENTICATION = 'Аутентификация'
AUTH_PREFIX = '/auth'
AUTH_JWT_PREFIX = '/auth/jwt'
DELETING_USERS_IS_PROHIBITED = 'Удаление пользователей запрещено!'
USERS = 'Пользователи'
USERS_ID_PATH = '/users/{id}'
USERS_PREFIX = '/users'

router = APIRouter()

router.include_router(
    fastapi_users.get_auth_router(auth_backend),
    prefix=AUTH_JWT_PREFIX,
    tags=[AUTHENTICATION],
)
router.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix=AUTH_PREFIX,
    tags=[AUTHENTICATION],
)
router.include_router(
    fastapi_users.get_users_router(UserRead, UserUpdate),
    prefix=USERS_PREFIX,
    tags=[USERS],
)


@router.delete(
    USERS_ID_PATH,
    summary=DELETING_USERS_IS_PROHIBITED,
    tags=[USERS],
    deprecated=True
)
def delete_user(id: str):
    """Не используйте удаление, деактивируйте пользователей."""
    raise HTTPException(
        status_code=HTTPStatus.METHOD_NOT_ALLOWED,
        detail=DELETING_USERS_IS_PROHIBITED
    )
