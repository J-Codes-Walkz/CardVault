"""URLs for the Contact page."""
from django.urls import path

from .views import ContactView

app_name = "contact"

urlpatterns = [
    path("", ContactView.as_view(), name="contact"),
]
