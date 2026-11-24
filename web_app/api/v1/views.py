from fastapi import APIRouter, Depends
from starlette import status
from starlette.responses import JSONResponse

from web_app.api.v1 import schemas
from web_app.core import health_utils
from web_app.core.dependencies import get_current_user
from web_app.core.settings import APP_SETTINGS

from web_app.celery import app

api_v1 = APIRouter(prefix='/api/v1', tags=['api-v1'])



@api_v1.get('/health/', response_model=schemas.HealthCheckResponse)
async def healthcheck():
    """ Health Check """
    ping_database, _ = await health_utils.ping_database()
    ping_redis, _ = await health_utils.ping_redis(APP_SETTINGS.redis_url)
    ping_celery, _ = health_utils.ping_celery(celery_app=app, ping_task='web_app.tasks.ping')

    total_status = all([ping_database, ping_redis, ping_celery])
    response = schemas.HealthCheckResponse(
        services={
            'database': ping_database,
            'ping_redis': ping_redis,
            'ping_celery': ping_celery
        },
        status=total_status,
    )
    http_status = status.HTTP_200_OK if total_status else status.HTTP_500_INTERNAL_SERVER_ERROR
    return JSONResponse(
        content=response.model_dump(by_alias=True),
        status_code=http_status
    )

