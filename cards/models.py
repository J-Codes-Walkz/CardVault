"""Catalogue models: card sets, cards and the reviews written on them."""
from django.conf import settings
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models


class CardSet(models.Model):
    """A released set of cards, for example Base Set."""

    name = models.CharField(max_length=100, unique=True)
    quantity = models.PositiveSmallIntegerField(
        help_text="How many cards are in the complete set."
    )

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name


class Card(models.Model):
    """One card in the shared catalogue. The same rows for every user."""

    class Rarity(models.TextChoices):
        COMMON = "COMMON", "Common"
        UNCOMMON = "UNCOMMON", "Uncommon"
        RARE = "RARE", "Rare"
        RARE_HOLO = "RARE_HOLO", "Rare Holo"

    name = models.CharField(max_length=100)
    card_set = models.ForeignKey(
        CardSet, on_delete=models.PROTECT, related_name="cards"
    )
    number = models.PositiveSmallIntegerField(
        help_text="The card's number within its set."
    )
    rarity = models.CharField(max_length=10, choices=Rarity.choices)
    market_price = models.DecimalField(
        max_digits=8, decimal_places=2, null=True, blank=True
    )
    image_url = models.URLField(blank=True)

    class Meta:
        ordering = ["card_set", "number"]
        constraints = [
            models.UniqueConstraint(
                fields=["card_set", "number"],
                name="unique_card_number_per_set",
            ),
        ]

    def __str__(self):
        return f"{self.name} ({self.card_set} #{self.number})"


class Review(models.Model):
    """A user's rating and written review of a card."""

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="reviews",
    )
    card = models.ForeignKey(
        Card, on_delete=models.CASCADE, related_name="reviews"
    )
    rating = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )
    body = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]
        constraints = [
            # A user reviews a card once, then edits that review.
            models.UniqueConstraint(
                fields=["user", "card"],
                name="unique_review_per_user_card",
            ),
            models.CheckConstraint(
                condition=models.Q(rating__gte=1, rating__lte=5),
                name="review_rating_between_1_and_5",
            ),
        ]

    def __str__(self):
        return f"{self.user} rated {self.card.name} {self.rating}/5"
