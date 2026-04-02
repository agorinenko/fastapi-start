import argparse
import os
from types import SimpleNamespace
from typing import Any

from alembic.config import Config
from sqlalchemy import create_engine, make_url, select, desc, NullPool
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy.orm import Session, sessionmaker

from db import models

from web_app.core.settings import APP_SETTINGS


def make_alembic_config(cmd_opts: argparse.Namespace | SimpleNamespace, db_url: str) -> Config:
    """ Создает объект конфигурации alembic """
    alembic_path = os.path.join(APP_SETTINGS.base_dir, 'alembic.ini')
    script_location = os.path.join(APP_SETTINGS.base_dir, 'db/alembic')
    cmd_opts.config = alembic_path
    alembic_cfg = Config(alembic_path, ini_section=cmd_opts.name, cmd_opts=cmd_opts)

    alembic_cfg.set_main_option('script_location', script_location)
    alembic_cfg.set_main_option('sqlalchemy.url', db_url)

    return alembic_cfg


def drop_all(url):
    """ Drop all tables stored in this metadata. """
    url = make_url(url)
    engine = create_engine(url)
    try:
        with engine.connect():
            models.Base.metadata.drop_all(engine)
    finally:
        engine.dispose()


async def get_or_create(db: AsyncSession, model, defaults: dict | None = None,
                        commit_if_create: bool | None = True, **kwargs) -> tuple[Any, bool]:
    """ Получение или создание записи """
    stmt = select(model).filter_by(**kwargs)
    result = await db.execute(stmt)
    instance = result.scalars().one_or_none()

    if instance:
        return instance, False
    else:
        defaults = defaults or {}
        kwargs.update(defaults)
        instance = model(**kwargs)
        db.add(instance)
        await db.flush()

        if commit_if_create:
            await db.commit()
            await db.refresh(instance)

        return instance, True


sync_engine = create_engine(APP_SETTINGS.sync_db_url,
                            pool_size=APP_SETTINGS.db_pool_size,
                            max_overflow=int(APP_SETTINGS.db_pool_size * 0.5),
                            pool_recycle=600,  # seconds, 10мин
                            pool_timeout=30,  # seconds
                            echo=True,
                            echo_pool='debug',
                            pool_use_lifo=True,
                            pool_pre_ping=True)
SyncSessionLocal = sessionmaker(sync_engine, expire_on_commit=False, autocommit=False, autoflush=False)

async_engine = create_async_engine(APP_SETTINGS.async_db_url,
                                   pool_size=APP_SETTINGS.db_pool_size,
                                   max_overflow=int(APP_SETTINGS.db_pool_size * 0.5),
                                   pool_recycle=600,  # seconds, 10мин
                                   pool_timeout=30,  # seconds
                                   echo=True,
                                   echo_pool='debug',
                                   pool_use_lifo=True,
                                   pool_pre_ping=True)
AsyncSessionLocal = async_sessionmaker(async_engine, expire_on_commit=False, autocommit=False, autoflush=False)

# Test env
sync_test_engine = create_engine(APP_SETTINGS.sync_db_test_url, poolclass=NullPool, echo=True,
                                 echo_pool='debug')
SyncTestSession = sessionmaker(sync_test_engine, expire_on_commit=False, autocommit=False, autoflush=False)

async_test_engine = create_async_engine(APP_SETTINGS.async_db_test_url, poolclass=NullPool, echo=True,
                                        echo_pool='debug')
AsyncTestSession = async_sessionmaker(async_test_engine, expire_on_commit=False, autocommit=False, autoflush=False)
