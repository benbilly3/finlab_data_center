#!/bin/bash
gunicorn finlab_data_center.wsgi:application --bind "0.0.0.0:$PORT" --env DJANGO_SETTINGS_MODULE=finlab_data_center.settings.$DJANGO_ENV & python manage.py qcluster --settings=finlab_data_center.settings.$DJANGO_ENV

