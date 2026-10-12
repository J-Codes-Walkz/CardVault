"""URLs for a user's own cards."""
from django.urls import path

from . import views

app_name = "collection"

urlpatterns = [
    path("", views.my_cards, name="my_cards"),
]
