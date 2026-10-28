"""URL configuration for the CardVault project."""
from django.contrib import admin
from django.shortcuts import redirect
from django.templatetags.static import static
from django.urls import include, path
from django.views.generic import TemplateView

from accounts.views import DeleteAccountView, SignupView
from accounts.views import admin_allowed, admin_login
from cards.views import HomeView

delete_account = DeleteAccountView.as_view()
privacy = TemplateView.as_view(template_name="privacy.html")


def favicon(request):
    """Browsers ask for /favicon.ico; point them at the real icon."""
    return redirect(static("images/favicon.ico"))


accessibility = TemplateView.as_view(template_name="accessibility.html")

# The admin's own login form has no limit on password guesses, so
# admin log ins go through django-allauth instead, and only
# superusers may use the admin at all.
admin.site.login = admin_login
admin.site.has_permission = admin_allowed
admin.site.site_header = "CardVault administration"
admin.site.site_title = "CardVault admin"
admin.site.index_title = "Manage CardVault"

urlpatterns = [
    path("favicon.ico", favicon),
    path("admin/", admin.site.urls),
    # Register, log in and log out are provided by django-allauth.
    # CardVault's own registration (with the age check) and account
    # deletion come before allauth's URLs, so they take priority.
    path("accounts/signup/", SignupView.as_view(), name="account_signup"),
    path("accounts/delete/", delete_account, name="delete_account"),
    path("accounts/", include("allauth.urls")),
    path("cards/mine/", include("collection.urls")),
    path("cards/", include("cards.urls")),
    path("contact/", include("contact.urls")),
    path("privacy/", privacy, name="privacy"),
    path("accessibility/", accessibility, name="accessibility"),
    path("", HomeView.as_view(), name="home"),
]
