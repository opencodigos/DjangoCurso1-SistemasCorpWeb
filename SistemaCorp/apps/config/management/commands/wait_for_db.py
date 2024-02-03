import time
import datetime  # Adicionado para usar o timeout

from psycopg2 import OperationalError as Psycopg2OpError
from django.db.utils import OperationalError
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    """Django command to wait for the database."""

    def handle(self, *args, **options):
        """Entrypoint for the command."""
        self.stdout.write('Waiting for the database...')
        db_up = False
        max_attempts = 30  # Defina o número desejado de tentativas
        attempt_count = 0

        # Defina o tempo máximo desejado em segundos
        timeout_seconds = 60
        start_time = datetime.datetime.now()

        while not db_up and attempt_count < max_attempts and (
                datetime.datetime.now() - start_time).seconds < timeout_seconds:
            try:
                self.check(databases=['default'])
                db_up = True
            except (Psycopg2OpError, OperationalError):
                attempt_count += 1
                self.stdout.write(f'Database unavailable, waiting 1 second... (Attempt {attempt_count})')
                time.sleep(1)

        if db_up:
            self.stdout.write(self.style.SUCCESS('Database available!'))
        else:
            self.stdout.write(self.style.ERROR('Database did not become available within the specified timeout.'))