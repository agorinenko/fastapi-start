import logging

from sqlalchemy import text

from db import db_utils

import redis.asyncio as redis

logger = logging.getLogger(__name__)


def ping_celery(celery_app, timeout: float | None = 5.0, ping_task: str | None = None) -> tuple[bool, Exception | None]:
    """ Проверка доступности celery """
    try:
        with celery_app.connection() as connection:
            connection.ensure_connection(timeout=timeout / 2)

        if ping_task:
            result = celery_app.send_task(ping_task).get(timeout=timeout)
            return result == 'pong', None

        return True, None
    except Exception as ex:
        logger.exception(ex)
        return False, ex


async def ping_database() -> tuple[bool, Exception | None]:
    """ Проверка доступности базы данных """
    try:
        async with db_utils.async_engine.connect() as con:
            result = await con.execute(text("SELECT 1"))
            test = result.scalar()
        return test == 1, None
    except Exception as ex:
        logger.exception(ex)
        return False, ex


async def ping_redis(url: str) -> tuple[bool, Exception | None]:
    """
    Проверка доступности Redis по URL.
    """
    try:
        async with redis.Redis.from_url(url, decode_responses=True, socket_connect_timeout=5, socket_timeout=5) as r:
            return await r.ping(), None

    except redis.ConnectionError as ex:
        logger.error(f'Redis connection error: {ex}')
        return False, ex
    except redis.TimeoutError as ex:
        logger.error(f'Redis timeout error: {ex}')
        return False, ex
    except Exception as ex:
        logger.exception(f'Unexpected Redis error: {ex}')
        return False, ex
