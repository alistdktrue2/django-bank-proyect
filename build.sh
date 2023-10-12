#!/usr/bin/env bash
# exit on error
set -o errexit

#poetry install
#pip install -r requirements.txt

python manage.py collectstatic --no-input
python manage.py migrate

python manage.py shell

from django.contrib.auth import get_user_model
User = get_user_model()
User.objects.create_superuser('alistdkadmin', 'alistdkadmin@gmail.com', '5179Backtrack*/')