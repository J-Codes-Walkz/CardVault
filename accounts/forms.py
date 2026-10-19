"""Account forms: allauth overrides and deleting an account."""
from allauth.account.forms import LoginForm as AllauthLoginForm
from allauth.account.forms import SignupForm as AllauthSignupForm
from django import forms
from django.utils import timezone

MINIMUM_AGE = 13
# Set in the session when someone gives an age under 13; registration
# then stays closed for that browser session.
UNDER_AGE_SESSION_KEY = "cardvault_signup_under_age"
TOO_YOUNG = "Sorry, you need to be 13 or older to create a CardVault account."
NOT_A_REAL_DATE = "Please enter your real date of birth."
# A message shown to the user, not a password.
WRONG_PASSWORD = "That password is not correct."  # nosec B105
DATE_OF_BIRTH_HELP = "Used only to check your age. It is not stored."
NO_EMAIL_USERNAME = "Please don't use an email address as your username: "
NO_EMAIL_USERNAME += "usernames are shown publicly next to your reviews."


def age_on(born, today):
    """Whole years between a date of birth and today."""
    had_birthday = (today.month, today.day) >= (born.month, born.day)
    return today.year - born.year - (0 if had_birthday else 1)


class LoginForm(AllauthLoginForm):
    """Log in form without the "Forgot your password?" link.

    Password reset works by email, and CardVault does not collect an
    email address, so the link would lead to a page nobody could use.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["password"].help_text = ""


class SignupForm(AllauthSignupForm):
    """Registration with an age check: under-13s cannot sign up.

    The form asks for a date of birth rather than "Are you 13 or
    older?", so it does not hint at the answer. The date is checked
    and then thrown away: there is no field to store it in.
    """

    date_of_birth = forms.DateField(
        label="Date of birth",
        help_text=DATE_OF_BIRTH_HELP,
        widget=forms.DateInput(attrs={"type": "date"}),
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.too_young = False
        order = ["username", "date_of_birth", "password1", "password2"]
        self.order_fields(order)

    def clean_username(self):
        username = super().clean_username()
        if "@" in username:
            raise forms.ValidationError(NO_EMAIL_USERNAME)
        return username

    def clean_date_of_birth(self):
        born = self.cleaned_data["date_of_birth"]
        today = timezone.localdate()
        if born > today or age_on(born, today) > 120:
            raise forms.ValidationError(NOT_A_REAL_DATE)
        if age_on(born, today) < MINIMUM_AGE:
            self.too_young = True
            raise forms.ValidationError(TOO_YOUNG)
        return born


class DeleteAccountForm(forms.Form):
    """Ask for the password before deleting an account."""

    password = forms.CharField(
        label="Your password",
        widget=forms.PasswordInput(attrs={"autocomplete": "current-password"}),
    )

    def __init__(self, *args, user=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.user = user

    def clean_password(self):
        password = self.cleaned_data["password"]
        if not self.user.check_password(password):
            raise forms.ValidationError(WRONG_PASSWORD)
        return password
