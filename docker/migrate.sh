#!/bin/sh
set +xeuo pipefail
cd /app
source venv/bin/activate
./manage.py migrate
