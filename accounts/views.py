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


def admin_login(request, extra_context=None):
    """Send every Django admin log in through django-allauth.

    Django admin's own login form has no limit on password guesses.
    allauth's has, so the admin's form is never shown: logged-out
    visitors go to the normal Log in page, staff go on to the admin,
    and logged-in users who are not staff are refused.
    """
    if not request.user.is_authenticated:
        login_url = reverse("account_login")
        return redirect_to_login(request.get_full_path(), login_url)
    if not request.user.is_staff:
        raise PermissionDenied
    next_url = request.GET.get("next", "")
    hosts = {request.get_host()}
    secure = request.is_secure()
    if url_has_allowed_host_and_scheme(next_url, hosts, secure):
        return redirect(next_url)
    return redirect("admin:index")


class SignupView(AllauthSignupView):
    """allauth's registration page, closed for the rest of the session
    to anyone who gives an age under 13, so they cannot simply go back
    and enter a different date."""

    def form_invalid(self, form):
        if getattr(form, "too_young", False):
            self.request.session[UNDER_AGE_SESSION_KEY] = True
            return redirect("account_signup")
        return super().form_invalid(form)


class DeleteAccountView(LoginMessageMixin, FormErrorMixin, FormView):
    """Permanently delete your account, cards and reviews."""

    form_class = DeleteAccountForm
    template_name = "accounts/delete_account.html"

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["user"] = self.request.user
        return kwargs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        context["entry_count"] = user.collection_entries.count()
        context["review_count"] = user.reviews.count()
        return context

    def form_valid(self, form):
        user = self.request.user
        logout(self.request)
        user.delete()
        messages.success(self.request, ACCOUNT_DELETED)
        return redirect("home")
