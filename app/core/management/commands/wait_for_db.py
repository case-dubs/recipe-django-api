# Django command to wait for database to be available
import time
from psycopg2 import OperationalError as Psycopg2OpError
from django.db.utils import OperationalError
from django.core.management.base import BaseCommand

class Command(BaseCommand):
    # Django command to wait for database
    # handle method will be called whenever we run command
    def handle(self, *args, **options):
        # Entrypoint for command. stdout is way to write things to screen
        self.stdout.write('Waiting for database...')
        db_up = False
        while db_up is False:
            try:
                self.check(databases=['default'])
                # no exceptions raised by line above, so we know database is up
                db_up = True
            except (Psycopg2OpError, OperationalError):
                self.stdout.write('Database unavailable, waiting 1 second...')
                time.sleep(1)
        self.stdout.write(self.style.SUCCESS('Database available!'))