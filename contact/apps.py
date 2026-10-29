"""App configuration for the Contact page."""
from django.apps import AppConfig


class ContactConfig(AppConfig):
    """Django settings for the contact app."""

    default_auto_field = 'django.db.models.BigAutoField'
    name = 'contact'
