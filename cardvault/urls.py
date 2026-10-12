"""URL configuration for the CardVault project."""
from django.contrib import admin
from django.urls import include, path
from django.views.generic import TemplateView

urlpatterns = [
    path("admin/", admin.site.urls),
    # Register, log in and log out are provided by django-allauth.
    path("accounts/", include("allauth.urls")),
    path("cards/mine/", include("collection.urls")),
    path("", TemplateView.as_view(template_name="home.html"), name="home"),
]
