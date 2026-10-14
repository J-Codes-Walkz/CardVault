"""Forms for the cards app."""
from django import forms

from .models import Review

RATING_CHOICES = [
    (1, "1 star"),
    (2, "2 stars"),
    (3, "3 stars"),
    (4, "4 stars"),
    (5, "5 stars"),
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
