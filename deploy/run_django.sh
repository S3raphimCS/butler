#!/bin/sh

set -e

python "manage.py" migrate --noinput

python "manage.py" collectstatic --noinput

python "manage.py" setup_tasks

python "manage.py" start_webhook

gunicorn -c "$PROJECT_ROOT/gunicorn.conf.py" butler_core.wsgi:application