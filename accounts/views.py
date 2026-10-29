"""Account views: admin log in, registration and account deletion."""
from allauth.account.views import SignupView as AllauthSignupView
from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth.views import redirect_to_login
from django.core.exceptions import PermissionDenied
from django.shortcuts import redirect
from django.urls import reverse
from django.utils.http import url_has_allowed_host_and_scheme
from django.views.generic import FormView

from .forms import UNDER_AGE_SESSION_KEY, DeleteAccountForm
from .mixins import FormErrorMixin, LoginMessageMixin

ACCOUNT_DELETED = "Your account, cards and reviews have been deleted."


def admin_allowed(request):
    """Return True only for active superusers (US28).

    Django lets any "staff" account use the admin by default; CardVault narrows
    that to superusers.
    """
    return request.user.is_active and request.user.is_superuser


def admin_login(request, extra_context=None):
    """Send every Django admin log in through django-allauth.

    Django admin's own login form has no limit on password guesses.
    allauth's has, so the admin's form is never shown: logged-out
    visitors go to the normal Log in page, superusers go on to the
    admin, and every other logged-in user is refused.
    """
    if not request.user.is_authenticated:
        login_url = reverse("account_login")
        return redirect_to_login(request.get_full_path(), login_url)
    if not admin_allowed(request):
        raise PermissionDenied
    next_url = request.GET.get("next", "")
    hosts = {request.get_host()}
    secure = request.is_secure()
    if url_has_allowed_host_and_scheme(next_url, hosts, secure):
        return redirect(next_url)
    return redirect("admin:index")


class SignupView(AllauthSignupView):
    """allauth's registration page, closed after an under-13 attempt.

    It stays closed for the rest of the browser session, so nobody can simply
    go back and enter a different date.
    """

    def form_invalid(self, form):
        """Close registration for the session after an under-13 attempt."""
        if getattr(form, "too_young", False):
            self.request.session[UNDER_AGE_SESSION_KEY] = True
            return redirect("account_signup")
        return super().form_invalid(form)


class DeleteAccountView(LoginMessageMixin, FormErrorMixin, FormView):
    """Permanently delete your account, cards and reviews."""

    form_class = DeleteAccountForm
    template_name = "accounts/delete_account.html"

    def get_form_kwargs(self):
        """Give the form the user, so it can check their password."""
        kwargs = super().get_form_kwargs()
        kwargs["user"] = self.request.user
        return kwargs

    def get_context_data(self, **kwargs):
        """Add how many entries and reviews will be deleted."""
        context = super().get_context_data(**kwargs)
        user = self.request.user
        context["entry_count"] = user.collection_entries.count()
        context["review_count"] = user.reviews.count()
        return context

    def form_valid(self, form):
        """Log out, delete the account and everything in it, and say so."""
        user = self.request.user
        logout(self.request)
        user.delete()
        messages.success(self.request, ACCOUNT_DELETED)
        return redirect("home")
