import argparse
import logging
import sys

from alembic.config import CommandLine

from db import db_utils
from web_app.core import settings


def main():
    logging.basicConfig(level=logging.DEBUG)

    alembic = CommandLine()
    alembic.parser.formatter_class = argparse.ArgumentDefaultsHelpFormatter
    options = alembic.parser.parse_args()

    config = db_utils.make_alembic_config(options, settings.APP_SETTINGS.async_db_url)
    sys.exit(alembic.run_cmd(config, options))


if __name__ == '__main__':
    main()