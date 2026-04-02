import uvicorn
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from log_config import init_log
from web_app.api.v1.views import api_v1
from web_app.core.settings import APP_SETTINGS

init_log()

app = FastAPI(title=APP_SETTINGS.project_name, docs_url='/swagger', debug=APP_SETTINGS.debug)
app.include_router(api_v1)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def run_server():
    """Запускает сервер Uvicorn."""
    uvicorn.run('main_app:app', host=APP_SETTINGS.server_host, port=APP_SETTINGS.server_port, reload=True)


if __name__ == '__main__':
    run_server()
