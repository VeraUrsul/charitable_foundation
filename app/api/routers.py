from fastapi import APIRouter

from app.api.endpoints import (
    charity_project_router, donation_router, google_api_router, user_router
)

CHARITY_PROJECT = 'Проекты для пожертвований'
CHARITY_PROJECT_PREFIX = '/charity_project'
DONATIONS = 'Пожертвования'
DONATIONS_PREFIX = '/donation'
GOOGLE = 'Google'
GOOGLE_PREFIX = '/google'

main_router = APIRouter()
main_router.include_router(
    charity_project_router,
    prefix=CHARITY_PROJECT_PREFIX,
    tags=[CHARITY_PROJECT]
)
main_router.include_router(
    donation_router, prefix=DONATIONS_PREFIX, tags=[DONATIONS]
)
main_router.include_router(
    google_api_router, prefix=GOOGLE_PREFIX, tags=[GOOGLE]
)
main_router.include_router(user_router)
