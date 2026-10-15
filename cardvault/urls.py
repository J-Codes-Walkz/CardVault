"""URL configuration for the CardVault project."""
from django.contrib import admin
from django.urls import include, path

from accounts.views import admin_login
from cards.views import HomeView

# The admin's own login form has no limit on password guesses, so
# admin log ins go through django-allauth instead.
admin.site.login = admin_login

urlpatterns = [
    path("admin/", admin.site.urls),
    # Register, log in and log out are provided by django-allauth.
    path("accounts/", include("allauth.urls")),
    path("cards/mine/", include("collection.urls")),
    path("cards/", include("cards.urls")),
    path("", HomeView.as_view(), name="home"),
]
