from fastapi import APIRouter, Depends


from web_app.api.v1 import schemas
from web_app.core import health_utils
from web_app.core.dependencies import get_current_user

api_v1 = APIRouter(prefix='/api/v1', tags=['api-v1'])



@api_v1.get('/health/', response_model=schemas.HealthCheckResponse)
async def healthcheck(current_user=Depends(get_current_user)):
    """ Health Check """
    ping_database, ex = await health_utils.ping_database()
    error_database = None
    if ex:
        error_database = str(ex)
    response = schemas.HealthCheckResponse(
        ping_database=ping_database,
        error_database=error_database,
        status=True,
        current_user=current_user
    )

    return response

