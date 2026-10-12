"""Customises django-allauth's wording to match CardVault's messages.

The exact text of every message is listed in
docs/notification-messages.md.
"""
from allauth.account.adapter import DefaultAccountAdapter

LOGGED_IN_TEMPLATE = "account/messages/logged_in.txt"
SIGNED_UP_TEMPLATE = "account/messages/signed_up.txt"


class AccountAdapter(DefaultAccountAdapter):
    """Account adapter with CardVault's own error and success text."""

    error_messages = {
        **DefaultAccountAdapter.error_messages,
        "username_taken": (
            "That username is already taken. Please choose another."
        ),
        # One message for both cases, so the form never reveals whether
        # it was the username or the password that was wrong.
        "username_password_mismatch": (
            "Invalid username or password. Please try again."
        ),
    }

    def post_login(self, request, user, **kwargs):
        """Remember whether this login is the end of a registration."""
        self.is_signup = kwargs.get("signup", False)
        return super().post_login(request, user, **kwargs)

    def add_message(self, request, level, message_template=None,
                    *args, **kwargs):
        """Greet a brand-new user differently from a returning one."""
        just_registered = getattr(self, "is_signup", False)
        if just_registered and message_template == LOGGED_IN_TEMPLATE:
            message_template = SIGNED_UP_TEMPLATE
        super().add_message(
            request, level, message_template, *args, **kwargs
        )
