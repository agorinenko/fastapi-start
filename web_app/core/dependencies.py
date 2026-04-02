import logging
from typing import AsyncGenerator

from fastapi import Depends, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from fastapi.security.utils import get_authorization_scheme_param
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status
from starlette.requests import Request
from starlette.status import HTTP_403_FORBIDDEN

from db import db_utils

logger = logging.getLogger(__name__)


class IamBearerAuth(HTTPBearer):
    def __init__(self, auto_error: bool | None = True):
        super().__init__(scheme_name='Bearer', auto_error=auto_error)

    async def __call__(self, request: Request) -> HTTPAuthorizationCredentials | None:
        authorization = request.headers.get('Authorization')
        scheme, credentials = get_authorization_scheme_param(authorization)
        if not (authorization and scheme and credentials):
            if self.auto_error:
                raise HTTPException(status_code=HTTP_403_FORBIDDEN, detail='Not authenticated')
            else:
                return None
        if scheme.lower() != 'bearer':
            if self.auto_error:
                raise HTTPException(status_code=HTTP_403_FORBIDDEN, detail='Invalid authentication credentials')
            else:
                return None
        return HTTPAuthorizationCredentials(scheme=scheme, credentials=credentials)


iam_security = IamBearerAuth()

_USERS = {
    '5c03f5957ade16a501c21fc56e97b8743630f15e0fb173276c561af32eeae8c8': {
        'id': '67e06366-6968-4b0c-9b56-f20ad0846bc8',
        'username': 'admin',
        'email': 'admin@example.com',
    },
    '03dd7f910f3d833b474125e8d1655fca8c89c80e92f3011e7deeaadaba7ca18d': {
        'id': '15f9e237-68a5-4de7-8de8-889ad7da7c66',
        'username': 'user1',
        'email': 'user1@example.com',
    },
    '78ac89d33772bb78048b857717f0acd79df3b543d22b9628ccdb9b666570c3bf': {
        'id': 'ade54ed6-d8ce-4a0b-8cbd-85d85d3b899b',
        'username': 'user2',
        'email': 'user2@example.com',
    },
}


async def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(iam_security)):
    if not credentials:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='Доступ запрещен.',
                            headers={'WWW-Authenticate': 'Bearer'})
    token = credentials.credentials
    scheme = credentials.scheme.lower()

    user = None
    if scheme == 'bearer':
        user = _USERS.get(token)

    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Реквизиты входа не действительны.',
                            headers={'WWW-Authenticate': scheme})

    return user


async def db_session() -> AsyncGenerator[AsyncSession]:
    async with db_utils.AsyncSessionLocal() as session:
        yield session


async def db_test_session() -> AsyncGenerator[AsyncSession]:
    async with db_utils.AsyncTestSession() as session:
        yield session
