"""URLs for a user's own cards."""
from django.urls import path

from .views import EntryCreate, EntryDelete, EntryEdit, MyCardsView

app_name = "collection"

urlpatterns = [
    path("", MyCardsView.as_view(), name="my_cards"),
    path("add/<int:card_pk>/", EntryCreate.as_view(), name="add_entry"),
    path("<int:pk>/edit/", EntryEdit.as_view(), name="edit_entry"),
    path("<int:pk>/remove/", EntryDelete.as_view(), name="delete_entry"),
]
