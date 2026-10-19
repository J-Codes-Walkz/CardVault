release: python manage.py migrate --noinput && python manage.py createcachetable && python manage.py clear_expired_cache
web: gunicorn cardvault.wsgi --worker-class gthread --threads 4 --max-requests 1000 --max-requests-jitter 100 --log-file -
