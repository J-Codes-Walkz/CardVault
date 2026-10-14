"""URLs for the card catalogue and reviews."""
from django.urls import include, path

from .views import CardDetailView, CardListView
from .views import ReviewCreate, ReviewDelete, ReviewEdit

app_name = "cards"

review_patterns = [
    path("edit/", ReviewEdit.as_view(), name="edit_review"),
    path("delete/", ReviewDelete.as_view(), name="delete_review"),
]

urlpatterns = [
    path("", CardListView.as_view(), name="card_list"),
    path("<int:pk>/", CardDetailView.as_view(), name="card_detail"),
    path("<int:card_pk>/review/", ReviewCreate.as_view(), name="add_review"),
    path("reviews/<int:pk>/", include(review_patterns)),
]
