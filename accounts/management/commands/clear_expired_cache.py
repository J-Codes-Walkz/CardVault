"""Delete expired rows from the database cache.

Django only clears expired cache rows once the table holds more than
300 entries, so on a quiet site the rate limit notes (which include
IP addresses) could stay in the database after they stop counting.
This command deletes them; the Procfile runs it on every release.
"""
from django.conf import settings
from django.core.management.base import BaseCommand
from django.db import connection
from django.utils import timezone


class Command(BaseCommand):
    help = "Delete expired rows from the database cache table."

    def handle(self, *args, **options):
        name = settings.CACHES["default"]["LOCATION"]
        table = connection.ops.quote_name(name)
        now = connection.ops.adapt_datetimefield_value(timezone.now())
        # A fixed statement: the table name comes from settings and the
        # time is passed as a parameter, so no user input reaches it.
        sql = f"DELETE FROM {table} WHERE expires < %s"  # nosec B608
        with connection.cursor() as cursor:
            cursor.execute(sql, [now])
            deleted = cursor.rowcount
        self.stdout.write(f"Deleted {deleted} expired cache entries.")
