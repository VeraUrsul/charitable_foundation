from copy import deepcopy
from datetime import datetime
from typing import List, Tuple

from aiogoogle import Aiogoogle

from app.core.config import settings

FORMAT = '%Y/%m/%d %H:%M:%S'
HEADER = [
    ['Отчёт от'],
    ['Топ проектов по скорости закрытия'],
    ['Название проекта', 'Время сбора', 'Описание']
]
MAX_COLUMN_COUNT = 11
MAX_ROW_COUNT = 100
NAME_OF_DOCUMENT = 'Отчёт от {time}'
NOT_ENOUGH_SPACE = (
    'Передаваемые данные не помещаются в таблице!'
    'Передано: столбцов {columns}, строк {rows}'
    f'Допустимо: столбцов {MAX_COLUMN_COUNT}, строк {MAX_ROW_COUNT}'
)
SPREADSHEET_BODY = dict(
    properties=dict(
        title='',
        locale='ru_RU'
    ),
    sheets=[
        dict(
            properties=dict(
                sheetType='GRID',
                sheetId=0,
                title='Лист1',
                gridProperties=dict(
                    rowCount=MAX_ROW_COUNT,
                    columnCount=MAX_COLUMN_COUNT
                )
            )
        )
    ]
)


async def spreadsheets_create(
    wrapper_services: Aiogoogle,
) -> Tuple[str, str]:
    service = await wrapper_services.discover('sheets', 'v4')
    spreadsheet_body = deepcopy(SPREADSHEET_BODY)
    spreadsheet_body['properties']['title'] = NAME_OF_DOCUMENT.format(
        time=datetime.now().strftime(FORMAT)
    )
    response = await wrapper_services.as_service_account(
        service.spreadsheets.create(json=spreadsheet_body)
    )
    return response['spreadsheetId'], response['spreadsheetUrl']


async def set_user_permissions(
    spreadsheetid: str,
    wrapper_services: Aiogoogle
) -> None:
    permissions_body = dict(
        type='user',
        role='writer',
        emailAddress=settings.email
    )
    service = await wrapper_services.discover('drive', 'v3')
    await wrapper_services.as_service_account(
        service.permissions.create(
            fileId=spreadsheetid, json=permissions_body, fields='id'
        )
    )


async def spreadsheets_update_value(
    spreadsheet_id: str,
    projects: List[dict],
    wrapper_services: Aiogoogle
) -> None:
    service = await wrapper_services.discover('sheets', 'v4')
    header = deepcopy(HEADER)
    header[0].append(datetime.now().strftime(FORMAT))
    projects = sorted(
        [
            dict(
                name=project.name,
                duration=project.close_date - project.create_date,
                description=project.description
            ) for project in projects
        ],
        key=lambda x: x['duration']
    )
    table_values = [
        *header,
        *[list(map(str, project.values())) for project in projects]
    ]
    update_body = dict(
        majorDimension='ROWS',
        values=table_values
    )
    column_count = max(map(len, table_values))
    row_count = len(table_values)
    if MAX_ROW_COUNT < row_count or MAX_COLUMN_COUNT < column_count:
        raise ValueError(
            NOT_ENOUGH_SPACE.format(
                columns=column_count,
                rows=row_count,
            )
        )
    await wrapper_services.as_service_account(
        service.spreadsheets.values.update(
            spreadsheetId=spreadsheet_id,
            range=f'R1C1:R{row_count}C{column_count}',
            valueInputOption='USER_ENTERED',
            json=update_body
        )
    )
