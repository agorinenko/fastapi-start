import datetime

from sqlalchemy import Column, Integer, String, DateTime, JSON, UUID, Enum, ForeignKey, Boolean, false
from sqlalchemy.orm import DeclarativeBase, relationship


def current_timestamp():
    """ Возвращает текущую дату и время в UTC 0 """
    return datetime.datetime.now(datetime.timezone.utc)


class Base(DeclarativeBase):
    pass

