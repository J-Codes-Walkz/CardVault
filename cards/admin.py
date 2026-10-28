"""Django admin registration for the catalogue models."""
from django.contrib import admin
from django.utils.html import format_html

from .models import Card, CardSet, Review

PREVIEW = '<img src="{}" alt="" width="120" height="167">'


@admin.register(CardSet)
class CardSetAdmin(admin.ModelAdmin):
    list_display = ("name", "quantity")
    search_fields = ("name",)


@admin.register(Card)
class CardAdmin(admin.ModelAdmin):
    list_display = ("name", "card_set", "number", "rarity")
    list_filter = ("card_set", "rarity")
    search_fields = ("name", "card_set__name")
    ordering = ("card_set", "number")
    list_per_page = 25
    readonly_fields = ("picture",)

    @admin.display(description="Picture")
    def picture(self, card):
        """The card's picture, so a corrected image link can be checked."""
        if not card.image_url:
            return "No picture link"
        return format_html(PREVIEW, card.image_url)


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ("card", "user", "rating", "created_at")
    list_filter = ("rating",)
    search_fields = ("card__name", "user__username", "body")
