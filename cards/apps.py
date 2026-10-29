"""App configuration for the card catalogue and reviews."""
from django.apps import AppConfig


class CardsConfig(AppConfig):
    """Django settings for the cards app."""

    default_auto_field = 'django.db.models.BigAutoField'
    name = 'cards'
