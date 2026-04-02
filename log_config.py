from pathlib import Path
import logging
import logging.config

from web_app.core.settings import APP_SETTINGS, parse_str_to_list

LOG_LEVEL = APP_SETTINGS.log_level
LOGGING_DEFAULT_HANDLER = parse_str_to_list(APP_SETTINGS.log_handler, default=['console'])
ENV_TYPE = APP_SETTINGS.env

Path(APP_SETTINGS.log_dir).mkdir(parents=True, exist_ok=True)

log_sql = APP_SETTINGS.log_sql
if log_sql:
    db_log_cfg = {
        'handlers': ['sql_console'],
        'level': LOG_LEVEL,
        'propagate': False,
    }
else:
    db_log_cfg = {
        'handlers': ['null'],
        'level': LOG_LEVEL,
        'propagate': False,
    }

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
    },
    'formatters': {
        'sql': {
            'format': '[SQL] %(levelname)s %(name)s %(asctime)s %(module)s %(message)s',
        },
        'default': {
            'format': '%(levelname)s %(name)s %(asctime)s %(module)s %(message)s',
        }
    },
    'handlers': {
        'file': {
            'class': 'logging.handlers.RotatingFileHandler',
            'maxBytes': 1024 * 1024 * 5,  # 5 MB
            'backupCount': 7,
            'filename': f'{APP_SETTINGS.log_dir}/{ENV_TYPE}.log',
            'formatter': 'default',
        },
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'default'
        },
        'sql_console': {
            'class': 'logging.StreamHandler',
            'formatter': 'sql'
        },
        'null': {
            'class': 'logging.NullHandler',
        }
    },
    'loggers': {
        '': {
            'handlers': LOGGING_DEFAULT_HANDLER,
            'level': LOG_LEVEL,
            'propagate': False,
        },
        'py.warnings': {
            'handlers': LOGGING_DEFAULT_HANDLER,
            'level': 'WARNING',
            'propagate': False,
        },
        'sqlalchemy.engine': db_log_cfg,
        'sqlalchemy.pool': {
            'handlers': LOGGING_DEFAULT_HANDLER,
            'level': 'WARNING',
            'propagate': False,
        },
        'sqlalchemy.dialects': {
            'handlers': LOGGING_DEFAULT_HANDLER,
            'level': 'WARNING',
            'propagate': False,
        }
    }
}


def init_log():
    logging.config.dictConfig(LOGGING)
