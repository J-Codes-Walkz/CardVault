# `settings.py` reference

The real file is `cardvault/settings.py`. This page explains the parts
of it that the checklist's security items depend on: no secrets in
source, `DEBUG` off in production, working authentication, and static
files served correctly on Heroku.

## Secrets and debug

```python
load_dotenv(BASE_DIR / ".env")

SECRET_KEY = os.environ["SECRET_KEY"]
DEBUG = os.environ.get("DEBUG", "False") == "True"

ALLOWED_HOSTS = [
    host for host in os.environ.get("ALLOWED_HOSTS", "").split(",") if host
]
if DEBUG:
    ALLOWED_HOSTS += ["localhost", "127.0.0.1"]
```

- **`SECRET_KEY` has no default**, so the app refuses to start with no
  key configured rather than silently falling back to an insecure one.
  This is what the checklist's "are any secret keys visible in source
  code" item is checking for.
- **`DEBUG` defaults to `False`**, so forgetting to set it on Heroku
  fails safe rather than fails open.
- **`.env` is local only.** It is listed in `.gitignore`;
  `.env.example` lists the variable names with no real values. On
  Heroku the same variables are config vars.

## Database

```python
DATABASES = {
    "default": dj_database_url.config(
        default=os.environ.get("DATABASE_URL"),
        conn_max_age=600,
        ssl_require=not DEBUG,
    )
}
```

`ssl_require=not DEBUG` enforces TLS to Heroku Postgres in production
without breaking a local connection that has no TLS configured.

## Authentication (django-allauth)

```python
INSTALLED_APPS = [
    # Django's own apps, then:
    "allauth",
    "allauth.account",
    "accounts",
    "cards",
    "collection",
]

AUTHENTICATION_BACKENDS = [
    "django.contrib.auth.backends.ModelBackend",
    "allauth.account.auth_backends.AuthenticationBackend",
]

ACCOUNT_ADAPTER = "accounts.adapter.AccountAdapter"
ACCOUNT_FORMS = {"login": "accounts.forms.LoginForm"}
ACCOUNT_LOGIN_METHODS = {"username"}
ACCOUNT_SIGNUP_FIELDS = ["username*", "password1*", "password2*"]
ACCOUNT_EMAIL_VERIFICATION = "none"
ACCOUNT_SESSION_REMEMBER = True

LOGIN_URL = "account_login"
LOGIN_REDIRECT_URL = "collection:my_cards"
LOGOUT_REDIRECT_URL = "home"
ACCOUNT_LOGOUT_REDIRECT_URL = "home"
```

- **Username and password only.** No email address is collected, so
  there is nothing to verify and no email service to configure.
- **`accounts.adapter.AccountAdapter`** replaces allauth's default
  wording with the messages in
  [notification-messages.md](./notification-messages.md).
- **`accounts.forms.LoginForm`** removes the "Forgot your password?"
  link, because password reset works by email.
- **`allauth.account.middleware.AccountMiddleware`** is the last entry
  in `MIDDLEWARE`, as allauth requires.
- **`AUTH_PASSWORD_VALIDATORS`** keeps all four of Django's
  validators with a minimum length of 8, which is what makes the
  "more complex password" part of US01 work.
- There is no `AUTH_USER_MODEL` setting: Django's built-in `User`
  model is used as-is.

## Static files

```python
if DEBUG or TESTING:
    STATICFILES_BACKEND = (
        "django.contrib.staticfiles.storage.StaticFilesStorage"
    )
else:
    STATICFILES_BACKEND = (
        "whitenoise.storage.CompressedManifestStaticFilesStorage"
    )
```

- **Whitenoise** serves CSS and images directly from the Django
  process on Heroku, whose filesystem is ephemeral and has no separate
  static file server. Its middleware sits straight after
  `SecurityMiddleware`.
- **The hashed-filename storage is production only.** It needs
  `collectstatic` to have run, which Heroku does on every build but a
  local `runserver` or `manage.py test` does not. `TESTING` is `True`
  while the test runner is active.

## Production-only hardening

```python
if not DEBUG and not TESTING:
    SECURE_SSL_REDIRECT = True
    SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    SECURE_HSTS_SECONDS = 31536000
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    SECURE_HSTS_PRELOAD = True
```

These only switch on when `DEBUG` is `False`, so local development
over plain HTTP still works. With them in place,
`python manage.py check --deploy` reports no issues.
