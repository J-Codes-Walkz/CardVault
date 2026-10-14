"""URL configuration for the CardVault project."""
from django.contrib import admin
from django.urls import include, path

from cards.views import HomeView

urlpatterns = [
    path("admin/", admin.site.urls),
    # Register, log in and log out are provided by django-allauth.
    path("accounts/", include("allauth.urls")),
    path("cards/mine/", include("collection.urls")),
    path("cards/", include("cards.urls")),
    path("", HomeView.as_view(), name="home"),
]
