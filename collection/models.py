"""The cards a user owns or wants."""
from django.conf import settings
from django.core.validators import MinValueValidator
from django.db import models

from cards.models import Card


class CollectionEntry(models.Model):
    """One card on one user's list, either owned or wanted."""

    class Status(models.TextChoices):
        """Whether a card is in the collection or on the wanted list."""

        OWNED = "OWNED", "Owned"
        WANTED = "WANTED", "Wanted"

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="collection_entries",
    )
    card = models.ForeignKey(
        Card, on_delete=models.CASCADE, related_name="collection_entries"
    )
    status = models.CharField(
        max_length=6, choices=Status.choices, default=Status.OWNED
    )
    quantity = models.PositiveIntegerField(
        default=1, validators=[MinValueValidator(1)]
    )
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]
        verbose_name_plural = "collection entries"
        constraints = [
            # A card is on a user's list once: owned or wanted, not both.
            models.UniqueConstraint(
                fields=["user", "card"],
                name="unique_entry_per_user_card",
            ),
            # "I no longer have this card" means deleting the entry.
            models.CheckConstraint(
                condition=models.Q(quantity__gte=1),
                name="entry_quantity_at_least_1",
            ),
        ]

    def __str__(self):
        """Whose entry it is, for example "ash: 2 x Charizard (Owned)"."""
        status = self.get_status_display()
        return f"{self.user}: {self.quantity} x {self.card.name} ({status})"
