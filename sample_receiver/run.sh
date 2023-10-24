#!/usr/bin/env bash

set -e

python manage.py migrate --noinput
python manage.py create_user_accounts
python manage.py create_oauth2_application
python manage.py create_test_access_token
pytest
python manage.py runserver 0.0.0.0:8100

