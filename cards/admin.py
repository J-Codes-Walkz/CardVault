"""Django admin registration for the catalogue models."""
from django.contrib import admin

from .models import Card, CardSet, Review


@admin.register(CardSet)
class CardSetAdmin(admin.ModelAdmin):
    list_display = ("name", "quantity")
    search_fields = ("name",)


@admin.register(Card)
class CardAdmin(admin.ModelAdmin):
    list_display = ("name", "card_set", "number", "rarity", "market_price")
    list_filter = ("card_set", "rarity")
    search_fields = ("name",)


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ("card", "user", "rating", "created_at")
    list_filter = ("rating",)
    search_fields = ("card__name", "user__username", "body")
