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

HOSTS = os.environ.get("ALLOWED_HOSTS", "")
ALLOWED_HOSTS = [host for host in HOSTS.split(",") if host]
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
    "contact",
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
    "cardvault.middleware.SecurityHeadersMiddleware",
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
# PostgreSQL everywhere. Heroku sets DATABASE_URL itself. Connections
# are encrypted (TLS) outside local development, reused for up to 10
# minutes, and checked before reuse in case the database restarted.
DATABASES = {
    "default": dj_database_url.config(
        default=os.environ.get("DATABASE_URL"),
        conn_max_age=600,
        conn_health_checks=True,
        ssl_require=not DEBUG,
    )
}
# Postgres stops any query still running after 10 seconds, so one slow
# request cannot hold the database while other visitors wait.
DATABASE_OPTIONS = DATABASES["default"].setdefault("OPTIONS", {})
DATABASE_OPTIONS["options"] = "-c statement_timeout=10000"

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# Cache in the database, so the log in rate limits below are shared by
# every web process and survive restarts. The table is created by
# `createcachetable` in the Procfile's release step.
CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.db.DatabaseCache",
        "LOCATION": "cardvault_cache",
    }
}

# --- Authentication (django-allauth) --------------------------------------
# Django's built-in User model is used as-is, so there is no
# AUTH_USER_MODEL setting.
AUTHENTICATION_BACKENDS = [
    "django.contrib.auth.backends.ModelBackend",
    "allauth.account.auth_backends.AuthenticationBackend",
]

ACCOUNT_ADAPTER = "accounts.adapter.AccountAdapter"
ACCOUNT_FORMS = {
    "login": "accounts.forms.LoginForm",
    "signup": "accounts.forms.SignupForm",
}
ACCOUNT_LOGIN_METHODS = {"username"}
ACCOUNT_SIGNUP_FIELDS = ["username*", "password1*", "password2*"]
# No email address is collected, so there is nothing to verify.
ACCOUNT_EMAIL_VERIFICATION = "none"
ACCOUNT_SESSION_REMEMBER = True

# Heroku's router sits in front of the app, so every request arrives
# from the router's own address. The router adds the visitor's real IP
# address as the last entry of X-Forwarded-For; trusting exactly one
# proxy makes allauth (and the Contact page) use that entry, so each
# "per IP address" limit applies to one visitor, not to everyone.
ALLAUTH_TRUSTED_PROXY_COUNT = 1
# Rate limits, stored in the shared database cache:
# - 3 wrong passwords lock that username for 15 minutes, whichever
#   addresses they came from, so a password cannot be guessed by
#   spreading attempts across many computers;
# - one IP address may get 5 passwords wrong a minute and 20 an hour,
#   across any usernames, which stops one computer trying thousands;
# - one IP address may try to log in 10 times a minute and register
#   10 accounts an hour.
ACCOUNT_RATE_LIMITS = {
    "login_failed": "5/m/ip,20/h/ip,3/15m/key",
    "login": "10/m/ip",
    "signup": "10/h/ip",
}

# Keep messages in the session, so the site sets no cookie beyond the
# two it needs (sessionid and csrftoken); see the privacy page.
MESSAGE_STORAGE = "django.contrib.messages.storage.session.SessionStorage"

LOGIN_URL = "account_login"
LOGIN_REDIRECT_URL = "collection:my_cards"
LOGOUT_REDIRECT_URL = "home"
ACCOUNT_LOGOUT_REDIRECT_URL = "home"

VALIDATION = "django.contrib.auth.password_validation"
AUTH_PASSWORD_VALIDATORS = [
    {"NAME": f"{VALIDATION}.UserAttributeSimilarityValidator"},
    {"NAME": f"{VALIDATION}.MinimumLengthValidator"},
    {"NAME": f"{VALIDATION}.CommonPasswordValidator"},
    {"NAME": f"{VALIDATION}.NumericPasswordValidator"},
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
STATIC_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"
if DEBUG or TESTING:
    STATIC_STORAGE = "django.contrib.staticfiles.storage.StaticFilesStorage"

STORAGES = {
    "default": {
        "BACKEND": "django.core.files.storage.FileSystemStorage",
    },
    "staticfiles": {
        "BACKEND": STATIC_STORAGE,
    },
}

# --- Logging ---------------------------------------------------------------
# Django only prints errors to the console when DEBUG is on, so on the
# live site a crash would leave no trace. Send warnings (such as 404s
# and refused requests) and errors (with their traceback) to the
# console, where Heroku's logs collect them. No passwords or form data
# are logged.
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {
        "console": {"class": "logging.StreamHandler"},
    },
    "loggers": {
        "django": {"handlers": ["console"], "level": "WARNING"},
    },
}
# Tests cause many 404s and refusals on purpose; keep them out of the
# test output. The tests that check logging capture it themselves.
if TESTING:
    LOGGING["handlers"]["console"] = {"class": "logging.NullHandler"}

# --- Production-only hardening ---------------------------------------------
if not DEBUG and not TESTING:
    SECURE_SSL_REDIRECT = True
    SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    CSRF_COOKIE_HTTPONLY = True
    SECURE_HSTS_SECONDS = 31536000
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    SECURE_HSTS_PRELOAD = True
