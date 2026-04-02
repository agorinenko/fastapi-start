import logging

from sqlalchemy import text

from db import db_utils

logger = logging.getLogger(__name__)


async def ping_database() -> tuple[bool, Exception | None]:
    """ Проверка доступности базы данных """
    try:
        async with db_utils.async_engine.connect() as con:
            result = await con.execute(text('SELECT 1'))
            test = result.scalar()
        return test == 1, None
    except Exception as ex:
        logger.exception(ex)
        return False, ex
