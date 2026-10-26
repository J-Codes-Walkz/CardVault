"""Forms for a user's own cards."""
from django import forms

from .models import CollectionEntry


class CollectionEntryForm(forms.ModelForm):
    """Status, quantity and notes for one card on a user's list."""

    class Meta:
        model = CollectionEntry
        fields = ["status", "quantity", "notes"]
        labels = {"status": "Owned or wanted?"}
        widgets = {
            "status": forms.RadioSelect,
            "quantity": forms.NumberInput(attrs={"min": 1}),
            "notes": forms.Textarea(attrs={"rows": 3}),
        }


class GotItForm(forms.ModelForm):
    """How many copies of a Wanted card you now own."""

    class Meta:
        model = CollectionEntry
        fields = ["quantity"]
        labels = {"quantity": "How many did you get?"}
        widgets = {"quantity": forms.NumberInput(attrs={"min": 1})}
