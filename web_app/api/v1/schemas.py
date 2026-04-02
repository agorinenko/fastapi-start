from typing import TypeVar, Generic

from pydantic import BaseModel

from web_app.core import utils


class CamelModel(BaseModel):
    class Config:
        alias_generator = utils.camelize
        validate_by_name = True


class UserResponse(CamelModel):
    username: str | None = None
    email: str | None = None


class HealthCheckResponse(CamelModel):
    """ Схема описания ответа запроса на проверку статуса сервиса """
    ping_database: bool
    status: bool
    error_database: str | None = None
    current_user: UserResponse | None = None



T = TypeVar('T')  # Обобщённый тип

class Meta(CamelModel):
    count: int | None = 0
    total_count: int | None = 0


class ListResponse(BaseModel, Generic[T]):
    meta: Meta | None = None
    list: list[T]
