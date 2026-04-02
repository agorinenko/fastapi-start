import re
from typing import Any

from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql.base import ExecutableOption


async def get_object_or_error(db: AsyncSession, model, status_code: int | None = 400,
                              detail: str | None = 'Объект не найден.',
                              options: list[ExecutableOption] | None = None,
                              order_by: Any | None = None, raise_error_if_none: bool | None = True,
                              **kwargs) -> Any | None:
    stmt = select(model)

    if options:
        stmt = stmt.options(*options)

    if order_by:
        if isinstance(order_by, list):
            stmt = stmt.order_by(*order_by)
        else:
            stmt = stmt.order_by(order_by)

    stmt = stmt.filter_by(**kwargs)

    result = await db.execute(stmt)
    item = result.scalars().one_or_none()
    if not item:
        if raise_error_if_none:
            raise HTTPException(status_code=status_code, detail=detail)

        return None

    return item


camelize_re = re.compile(r'[a-z0-9]?_[a-z0-9]')


def camelize(data):
    if isinstance(data, str) and "_" in data:
        return re.sub(camelize_re, _underscore_to_camel, data)

    return data


def _underscore_to_camel(match):
    group = match.group()
    if len(group) == 3:
        return group[0] + group[2].upper()
    else:
        return group[1].upper()
