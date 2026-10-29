"""Django admin registration for collection entries."""
from django.contrib import admin

from .models import CollectionEntry


@admin.register(CollectionEntry)
class CollectionEntryAdmin(admin.ModelAdmin):
    """My Cards entries in the admin, filtered by status or set."""

    list_display = ("user", "card", "status", "quantity", "created_at")
    list_filter = ("status", "card__card_set")
    search_fields = ("user__username", "card__name")
