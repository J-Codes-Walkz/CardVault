release: python manage.py migrate --noinput && python manage.py createcachetable
web: gunicorn cardvault.wsgi --log-file -
