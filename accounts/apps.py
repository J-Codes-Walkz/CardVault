"""App configuration for accounts: register, log in, delete an account."""
from django.apps import AppConfig


class AccountsConfig(AppConfig):
    """Django settings for the accounts app."""

    default_auto_field = 'django.db.models.BigAutoField'
    name = 'accounts'
