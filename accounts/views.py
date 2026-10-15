"""Account views."""
from django.contrib.auth.views import redirect_to_login
from django.core.exceptions import PermissionDenied
from django.shortcuts import redirect
from django.urls import reverse
from django.utils.http import url_has_allowed_host_and_scheme


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
