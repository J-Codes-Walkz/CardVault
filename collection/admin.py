"""Django admin registration for collection entries."""
from django.contrib import admin

from .models import CollectionEntry


@admin.register(CollectionEntry)
class CollectionEntryAdmin(admin.ModelAdmin):
    list_display = ("user", "card", "status", "quantity", "created_at")
    list_filter = ("status",)
    search_fields = ("user__username", "card__name")
