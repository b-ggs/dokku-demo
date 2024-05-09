release: python3 manage.py migrate
web: gunicorn dokku_demo.wsgi:application
celery: celery -A dokku_demo worker -l info
