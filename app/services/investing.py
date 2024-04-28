from datetime import datetime
from typing import List

from app.models.abstract import BaseAbstractAmount


def investment_process(
        target: BaseAbstractAmount,
        sources: List[BaseAbstractAmount],
) -> List[BaseAbstractAmount]:
    changes = []
    for source in sources:
        amount = min(
            target.full_amount - target.invested_amount,
            source.full_amount - source.invested_amount
        )
        if not amount:
            break
        for object in [source, target]:
            object.invested_amount += amount
            if object.full_amount == object.invested_amount:
                object.fully_invested = True
                object.close_date = datetime.now()
        changes.append(source)
    return changes
