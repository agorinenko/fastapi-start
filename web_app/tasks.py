import logging

from log_config import init_log
from web_app.celery import app

logger = logging.getLogger(__name__)

init_log()
