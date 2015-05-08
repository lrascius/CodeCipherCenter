web: python csc473/manage.py collectstatic --noinput; bin/gunicorn_django --workers=1 --bind=0.0.0.0:$PORT csc473/settings.py
