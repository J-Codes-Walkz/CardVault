"""Forms for the cards app."""
from django import forms

from .models import Review

RATING_CHOICES = [
    (1, "1 Poké Ball"),
    (2, "2 Poké Balls"),
    (3, "3 Poké Balls"),
    (4, "4 Poké Balls"),
    (5, "5 Poké Balls"),
]


class ReviewForm(forms.ModelForm):
    """A 1 to 5 star rating and a written review of a card."""

    rating = forms.TypedChoiceField(
        choices=RATING_CHOICES,
        coerce=int,
        widget=forms.RadioSelect,
        label="Rating",
    )

    class Meta:
        model = Review
        fields = ["rating", "body"]
        labels = {"body": "Your review"}
        widgets = {"body": forms.Textarea(attrs={"rows": 4})}
