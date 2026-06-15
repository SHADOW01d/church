"""Development settings: convenient, never for production."""

from .base import *  # noqa: F401,F403
from .base import STORAGES, env

DEBUG = env.bool("DEBUG", default=True)

# Serve static files directly in development (no manifest/collectstatic step).
STORAGES = {
    **STORAGES,
    "staticfiles": {
        "BACKEND": "django.contrib.staticfiles.storage.StaticFilesStorage",
    },
}

ALLOWED_HOSTS = env.list(
    "DJANGO_ALLOWED_HOSTS",
    default=["localhost", "127.0.0.1", "0.0.0.0"],
)

# A throwaway key so the app boots locally without extra setup. Never used
# in production, where DJANGO_SECRET_KEY must be provided by the environment.
SECRET_KEY = env(
    "DJANGO_SECRET_KEY",
    default="django-insecure-dev-only-key-change-me-0123456789abcdef",
)

# Print emails to the console during development.
EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"
