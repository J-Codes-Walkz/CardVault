"""Form overrides for django-allauth."""
from allauth.account.forms import LoginForm as AllauthLoginForm


class LoginForm(AllauthLoginForm):
    """Log in form without the "Forgot your password?" link.

    Password reset works by email, and CardVault does not collect an
    email address, so the link would lead to a page nobody could use.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["password"].help_text = ""
