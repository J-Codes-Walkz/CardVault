"""View mixins shared by every app that has private pages or forms."""
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin

LOGIN_NEEDED = "Please log in to view that page."
FORM_ERRORS = "Please correct the errors below and try again."


class LoginMessageMixin(LoginRequiredMixin):
    """Send logged-out visitors to the log in page and tell them why."""

    def handle_no_permission(self):
        """Tell a logged-out visitor why they were sent to the log in page."""
        if not self.request.user.is_authenticated:
            messages.info(self.request, LOGIN_NEEDED)
        return super().handle_no_permission()


class FormErrorMixin:
    """Show one error message above any form that fails validation."""

    def form_invalid(self, form):
        """Add the error message, then show the form again with its errors."""
        messages.error(self.request, FORM_ERRORS)
        return super().form_invalid(form)
