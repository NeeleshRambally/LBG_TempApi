# test_settings.py

from .settings import *  # Import all settings from the base settings file

# Override database settings for tests
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',  # Use SQLite for fast in-memory database
        'NAME': ':memory:',
    }
}

# Disable CORS headers in testing
CORS_ORIGIN_ALLOW_ALL = False

# Use a simpler password hasher for faster tests
PASSWORD_HASHERS = [
    'django.contrib.auth.hashers.MD5PasswordHasher',
]

# Disable logging for tests
LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
}
