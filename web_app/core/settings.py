from pathlib import Path

from dotenv import load_dotenv
from pydantic import Field
from pydantic_settings import BaseSettings

load_dotenv()

BASE_DIR = Path(__file__).parents[2]


class AppSettings(BaseSettings):
    """ Конфигурация сервиса """

    # Common
    project_name: str = 'REST API'
    env: str = Field(alias='ENV', default='PROD')
    debug: bool = Field(alias='DEBUG', default=False)
    log_level: str = Field(alias='LOGGING_DEFAULT_LEVEL', default='INFO')
    log_handler: str = Field(alias='LOGGING_DEFAULT_HANDLER', default='console')
    server_port: int = Field(alias='SERVER_PORT', default=8000)
    server_host: str = Field(alias='SERVER_HOST', default='localhost')

    # Data base
    db_name: str = Field(alias='POSTGRES_DB', default='')
    db_user: str = Field(alias='POSTGRES_USER', default='')
    db_password: str = Field(alias='POSTGRES_PASSWORD', default='')
    db_host: str = Field(alias='DB_HOST', default='localhost')
    db_port: str = Field(alias='DB_PORT', default='5432')
    db_pool_size: int = Field(alias='POOL_SIZE', default=5)
    log_sql: bool = Field(alias='LOG_SQL', default=False)

    # Redis
    redis_host: str = Field(alias='REDIS_HOST', default='localhost')
    redis_port: int = Field(alias='REDIS_PORT', default=6379)
    redis_channel: int = Field(alias='REDIS_CHANNEL', default=1)
    redis_user: str = Field(alias='REDIS_USER', default='')
    redis_password: str = Field(alias='REDIS_PASSWORD', default='')

    # Celery
    celery_eager: bool = Field(alias='CELERY_EAGER', default=False)
    visibility_timeout_in_sec: int = Field(alias='VISIBILITY_TIMEOUT_IN_SEC', default=3600)
    key_prefix: str = Field(alias='KEY_PREFIX', default='pay')
    broker_pool_limit: int = Field(alias='BROKER_POOL_LIMIT', default=10)
    task_acks_late: bool = Field(alias='TASK_ACKS_LATE', default=False)
    task_reject_on_worker_lost: bool = Field(alias='TASK_REJECT_ON_WORKER_LOST', default=False)
    task_acks_on_failure: bool = Field(alias='TASK_ACKS_ON_FAILURE', default=True)
    celery_concurrency: int = Field(alias='CELERY_CONCURRENCY', default=5)
    worker_prefetch_multiplier: int = Field(alias='WORKER_PREFETCH_MULTIPLIER', default=4)
    worker_hijack_root_logger: bool = Field(alias='CELERY_HIJACK_ROOT_LOGGER', default=False)

    broker_connection_max_retries: int = Field(alias='BROKER_CONNECT_MAX_RETRIES', default=100)
    broker_connection_timeout: int = Field(alias='BROKER_CONNECT_TIMEOUT', default=30)
    broker_heartbeat: int = Field(alias='BROKER_HEARTBEAT', default=120)
    broker_heartbeat_checkrate: float = Field(alias='BROKER_HEARTBEAT_CHECKRATE', default=2.0)
    broker_heartbeat_interval: int = Field(alias='BROKER_HEARTBEAT_INTERVAL', default=30)

    # Kafka
    topic_name: str = Field(alias='TOPIC_NAME', default='default-channel')
    kafka_bootstrap_servers: str = Field(alias='KAFKA_BOOTSTRAP_SERVERS', default='localhost:9092')
    servers_group_id: str = Field(alias='SERVERS_GROUP_ID', default='web_group0')
    server_id: str = Field(alias='SERVER_ID', default='web_srv0')
    security_protocol: str = Field(alias='SECURITY_PROTOCOL', default='PLAINTEXT')
    sasl_mechanism: str = Field(alias='SASL_MECHANISM', default='PLAIN')
    sasl_plain_username: str | None = Field(alias='SASL_PLAIN_USERNAME', default=None)
    sasl_plain_password: str | None = Field(alias='SASL_PLAIN_PASSWORD', default=None)
    kafka_session_timeout_ms: int = Field(alias='KAFKA_SESSION_TIMEOUT_MS', default=10000)
    kafka_max_poll_interval_ms: int = Field(alias='KAFKA_MAX_POLL_INTERVAL_MS', default=300000)
    kafka_auto_offset_reset: str = Field(alias='KAFKA_AUTO_OFFSET_RESET', default='latest')

    @property
    def celery_broker_url(self) -> str:
        return self.redis_url

    @property
    def redis_url(self) -> str:
        return f'redis://{self.redis_user}:{self.redis_password}@{self.redis_host}:{self.redis_port}/{self.redis_channel}'

    @property
    def async_db_url(self) -> str:
        return f'postgresql+asyncpg://{self.db_user}:{self.db_password}@{self.db_host}:{self.db_port}/{self.db_name}'

    @property
    def async_db_test_url(self) -> str:
        return f'postgresql+asyncpg://{self.db_user}:{self.db_password}@{self.db_host}:{self.db_port}/test_{self.db_name}'

    @property
    def sync_db_url(self) -> str:
        return f'postgresql://{self.db_user}:{self.db_password}@{self.db_host}:{self.db_port}/{self.db_name}'

    @property
    def sync_db_test_url(self) -> str:
        return f'postgresql://{self.db_user}:{self.db_password}@{self.db_host}:{self.db_port}/test_{self.db_name}'

    @property
    def base_dir(self) -> Path:
        return BASE_DIR

    @property
    def log_dir(self) -> Path:
        return BASE_DIR / 'logs'


APP_SETTINGS = AppSettings()


def parse_str_to_list(param_value: str, default: list[str] | str | None = None,
                      separator: str | None = ',') -> list[str] | str | None:
    """
    Преобразование строки в список
    :param param_value: значение переменной окружения
    :param default: значение по умолчанию
    :param separator: разделитель
    :return:
    """
    if default and isinstance(default, str):
        default = [default]

    return [v for v in param_value.split(separator) if v] if param_value else default
