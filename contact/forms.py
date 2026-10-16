"""The Contact page form."""
from django import forms

from .models import ContactMessage

MESSAGE_HELP = "Up to 2,000 characters. Please don't include passwords."


class ContactForm(forms.ModelForm):
    """Name, email and message, plus a hidden trap field for bots.

    People never see the "website" field, as CSS hides it, but bots
    that fill in every field do; their messages are thrown away.
    """

    website = forms.CharField(required=False, label="Leave this empty")

    class Meta:
        model = ContactMessage
        fields = ["name", "email", "message"]
        labels = {"name": "Your name", "email": "Your email address"}
        help_texts = {"message": MESSAGE_HELP}
        widgets = {
            "name": forms.TextInput(attrs={"autocomplete": "name"}),
            "email": forms.EmailInput(attrs={"autocomplete": "email"}),
            "message": forms.Textarea(attrs={"rows": 6}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        trap = self.fields["website"].widget.attrs
        trap.update({"autocomplete": "off", "tabindex": "-1"})

    def is_spam(self):
        """True when the hidden trap field was filled in."""
        return bool(self.cleaned_data.get("website"))
