import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

INSTALLED_APPS = [
    "django.contrib.contenttypes",
    "django.contrib.auth",
    "render_block",
]

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": ":memory:",
    }
}

SECRET_KEY = "test_secret_key"

TEMPLATES = [
    {
        "BACKEND": "render_block.backend.Jinja2",
        "DIRS": [os.path.join(BASE_DIR, "tests", "templates")],
        "APP_DIRS": False,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
            ],
        },
    },
]

USE_TZ = True
