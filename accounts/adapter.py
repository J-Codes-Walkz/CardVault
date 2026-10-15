"""Customises django-allauth's wording to match CardVault's messages.

The exact text of every message is listed in
docs/NOTIFICATION_MESSAGES.md.
"""
from allauth.account.adapter import DefaultAccountAdapter

from .forms import UNDER_AGE_SESSION_KEY

LOGGED_IN_TEMPLATE = "account/messages/logged_in.txt"
SIGNED_UP_TEMPLATE = "account/messages/signed_up.txt"

USERNAME_TAKEN = "That username is already taken. Please choose another."
LOGIN_FAILED = "Invalid username or password. Please try again."


class AccountAdapter(DefaultAccountAdapter):
    """Account adapter with CardVault's own error and success text."""

    error_messages = {
        **DefaultAccountAdapter.error_messages,
        "username_taken": USERNAME_TAKEN,
        # One message for both cases, so the form never reveals whether
        # it was the username or the password that was wrong.
        "username_password_mismatch": LOGIN_FAILED,
    }

    def is_open_for_signup(self, request):
        """Close registration for a browser that gave an age under 13."""
        return not request.session.get(UNDER_AGE_SESSION_KEY, False)

    def post_login(self, request, user, **kwargs):
        """Remember whether this login is the end of a registration."""
        self.is_signup = kwargs.get("signup", False)
        return super().post_login(request, user, **kwargs)

    def add_message(self, request, level, template=None, *args, **kwargs):
        """Greet a brand-new user differently from a returning one."""
        just_registered = getattr(self, "is_signup", False)
        if just_registered and template == LOGGED_IN_TEMPLATE:
            template = SIGNED_UP_TEMPLATE
        super().add_message(request, level, template, *args, **kwargs)
