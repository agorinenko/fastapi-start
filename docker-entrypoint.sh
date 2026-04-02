#!/bin/bash
set -e

./wait-for-it.sh "$DB_HOST":"$DB_PORT"
./wait-for-it.sh "$REDIS_HOST":"$REDIS_PORT"

case "$1" in
    web)
      python -m db upgrade head
      exec supervisord -c /opt/app/supervisord.conf
      ;;
    celery)
      exec celery -A web_app worker --loglevel=debug -E --pool=threads
      ;;
    beat)
      exec celery -A web_app beat -l debug
      ;;
    *)
      exec "$@"
      ;;
esac
