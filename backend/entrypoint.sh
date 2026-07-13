#!/bin/bash
set -e

python src/manage.py migrate --noinput

exec "$@"
