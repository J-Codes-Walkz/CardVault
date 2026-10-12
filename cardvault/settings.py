"""Django settings for the CardVault project.

Every secret is read from an environment variable: a local `.env`
file in development (never committed) and config vars on Heroku.
"""
import os
import sys
from pathlib import Path

import dj_database_url
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(BASE_DIR / ".env")

# True while `python manage.py test` is running.
TESTING = "test" in sys.argv

# --- Secrets and debug ---------------------------------------------------
# No default: the app refuses to start without a key rather than
# falling back to an insecure one.
SECRET_KEY = os.environ["SECRET_KEY"]

# Off unless explicitly switched on, so a missing variable fails safe.
DEBUG = os.environ.get("DEBUG", "False") == "True"

ALLOWED_HOSTS = [
    host for host in os.environ.get("ALLOWED_HOSTS", "").split(",") if host
]
if DEBUG:
    ALLOWED_HOSTS += ["localhost", "127.0.0.1"]

# --- Apps ----------------------------------------------------------------
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "allauth",
    "allauth.account",
    "accounts",
    "cards",
    "collection",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    # Whitenoise must come straight after SecurityMiddleware.
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "allauth.account.middleware.AccountMiddleware",
]

ROOT_URLCONF = "cardvault.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "cardvault.wsgi.application"

# --- Database ------------------------------------------------------------
# PostgreSQL everywhere. Heroku sets DATABASE_URL itself.
DATABASES = {
    "default": dj_database_url.config(
        default=os.environ.get("DATABASE_URL"),
        conn_max_age=600,
        ssl_require=not DEBUG,
    )
}

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# --- Authentication (django-allauth) --------------------------------------
# Django's built-in User model is used as-is, so there is no
# AUTH_USER_MODEL setting.
AUTHENTICATION_BACKENDS = [
    "django.contrib.auth.backends.ModelBackend",
    "allauth.account.auth_backends.AuthenticationBackend",
]

ACCOUNT_ADAPTER = "accounts.adapter.AccountAdapter"
ACCOUNT_FORMS = {"login": "accounts.forms.LoginForm"}
ACCOUNT_LOGIN_METHODS = {"username"}
ACCOUNT_SIGNUP_FIELDS = ["username*", "password1*", "password2*"]
# No email address is collected, so there is nothing to verify.
ACCOUNT_EMAIL_VERIFICATION = "none"
ACCOUNT_SESSION_REMEMBER = True

LOGIN_URL = "account_login"
LOGIN_REDIRECT_URL = "collection:my_cards"
LOGOUT_REDIRECT_URL = "home"
ACCOUNT_LOGOUT_REDIRECT_URL = "home"

AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation."
             "UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation."
             "MinimumLengthValidator",
     "OPTIONS": {"min_length": 8}},
    {"NAME": "django.contrib.auth.password_validation."
             "CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation."
             "NumericPasswordValidator"},
]

# --- Internationalisation -------------------------------------------------
LANGUAGE_CODE = "en-gb"
TIME_ZONE = "Europe/London"
USE_I18N = True
USE_TZ = True

# --- Static files (served by Whitenoise on Heroku) -------------------------
STATIC_URL = "static/"
STATIC_ROOT = BASE_DIR / "staticfiles"
STATICFILES_DIRS = [BASE_DIR / "static"]

# The hashed-filename storage needs `collectstatic` to have run, which
# is true on Heroku but not in local development or the test runner.
if DEBUG or TESTING:
    STATICFILES_BACKEND = (
        "django.contrib.staticfiles.storage.StaticFilesStorage"
    )
else:
    STATICFILES_BACKEND = (
        "whitenoise.storage.CompressedManifestStaticFilesStorage"
    )

STORAGES = {
    "default": {
        "BACKEND": "django.core.files.storage.FileSystemStorage",
    },
    "staticfiles": {
        "BACKEND": STATICFILES_BACKEND,
    },
}

# --- Production-only hardening ---------------------------------------------
if not DEBUG and not TESTING:
    SECURE_SSL_REDIRECT = True
    SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    SECURE_HSTS_SECONDS = 31536000
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    SECURE_HSTS_PRELOAD = True
