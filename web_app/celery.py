from celery import Celery

from log_config import init_log
from web_app.beat import beat_schedule
from web_app.core.settings import APP_SETTINGS

app = Celery('web_app', broker=APP_SETTINGS.celery_broker_url)
app.autodiscover_tasks()
import web_app.tasks  # 👈 ОБЯЗАТЕЛЬНО!

init_log()

transport_options = {
    'visibility_timeout': APP_SETTINGS.visibility_timeout_in_sec,
    'global_keyprefix': APP_SETTINGS.key_prefix,
    'retry_on_timeout': True,
    'socket_keepalive': True,
    'socket_timeout': APP_SETTINGS.broker_connection_timeout,
    'socket_connect_timeout': APP_SETTINGS.broker_connection_timeout,
    'health_check_interval': APP_SETTINGS.broker_heartbeat_interval,
    'max_connections': APP_SETTINGS.broker_pool_limit,
    'retry_on_error': [ConnectionError, TimeoutError, OSError],
    'retry_policy': {
        'max_retries': APP_SETTINGS.broker_connection_max_retries,
        'interval_start': 0.5,
        'interval_step': 1,
        'interval_max': 60,
    }
}

app.conf.update(
    timezone='UTC',
    beat_dburi=APP_SETTINGS.sync_db_url,
    beat_schedule=beat_schedule,
    worker_hijack_root_logger=APP_SETTINGS.worker_hijack_root_logger,
    accept_content=['json'],
    broker_transport_options=transport_options,
    broker_pool_limit=APP_SETTINGS.broker_pool_limit,
    result_backend=APP_SETTINGS.celery_broker_url,
    result_backend_transport_options=transport_options,
    result_serializer='json',
    task_acks_late=APP_SETTINGS.task_acks_late,
    task_always_eager=APP_SETTINGS.celery_eager,
    task_serializer='json',
    task_reject_on_worker_lost=APP_SETTINGS.task_reject_on_worker_lost,
    task_acks_on_failure_or_timeout=APP_SETTINGS.task_acks_on_failure,
    worker_state_db=str(APP_SETTINGS.base_dir / 'celery-state'),
    worker_concurrency=APP_SETTINGS.celery_concurrency,
    worker_prefetch_multiplier=APP_SETTINGS.worker_prefetch_multiplier,
    broker_connection_retry_on_startup=True,
    broker_connection_retry=True,
    broker_connection_max_retries=None,
    broker_connection_timeout=APP_SETTINGS.broker_connection_timeout,
    # Эти настройки не работают с Redis! Они предназначены только для RabbitMQ
    # broker_heartbeat=APP_SETTINGS.broker_heartbeat,
    # broker_heartbeat_checkrate=APP_SETTINGS.broker_heartbeat_checkrate
)
