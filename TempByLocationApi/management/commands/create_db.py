from django.core.management.base import BaseCommand
from django.conf import settings
import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

class Command(BaseCommand):
    help = 'Creates the PostgreSQL database if it does not exist'

    def handle(self, *args, **options):
        db_name = settings.DATABASES['default']['NAME']
        db_user = settings.DATABASES['default']['USER']
        db_password = settings.DATABASES['default']['PASSWORD']
        db_host = settings.DATABASES['default']['HOST']
        db_port = settings.DATABASES['default']['PORT']

        try:
            # Connect to PostgreSQL
            conn = psycopg2.connect(
                dbname='postgres',
                user=db_user,
                password=db_password,
                host=db_host,
                port=db_port
            )
            conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
            cursor = conn.cursor()

            # Check if the database exists
            cursor.execute(f"SELECT 1 FROM pg_database WHERE datname = '{db_name}';")
            exists = cursor.fetchone()

            if not exists:
                self.stdout.write(self.style.SUCCESS(f'Creating database "{db_name}"...'))
                cursor.execute(f"CREATE DATABASE {db_name};")
                self.stdout.write(self.style.SUCCESS(f'Database "{db_name}" created successfully!'))
            else:
                self.stdout.write(self.style.WARNING(f'Database "{db_name}" already exists.'))

            # Close the cursor and connection
            cursor.close()
            conn.close()

        except Exception as e:
            self.stderr.write(self.style.ERROR(f'Error creating database: {str(e)}'))
