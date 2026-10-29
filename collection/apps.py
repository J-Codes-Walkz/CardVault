"""App configuration for My Cards: each user's owned and wanted cards."""
from django.apps import AppConfig


class CollectionConfig(AppConfig):
    """Django settings for the collection app."""

    default_auto_field = 'django.db.models.BigAutoField'
    name = 'collection'
