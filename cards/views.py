"""Views for the home page, the card catalogue and card reviews."""
from django.contrib import messages
from django.db.models import Avg, Count
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse
from django.utils.functional import cached_property
from django.views.generic import CreateView, DeleteView, DetailView
from django.views.generic import ListView, TemplateView, UpdateView

from accounts.mixins import FormErrorMixin, LoginMessageMixin
from collection.forms import CollectionEntryForm

from .forms import ReviewForm
from .models import Card

REVIEW_ADDED = "Thank you for submitting your review!"
REVIEW_UPDATED = "Your review was updated successfully."
REVIEW_DELETED = "Your review was deleted."
REVIEW_EXISTS = "You have already reviewed {card}. You can edit it here."


class HomeView(TemplateView):
    """The landing page, with a row of featured cards."""

    template_name = "home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cards = Card.objects.select_related("card_set")
        context["featured_cards"] = cards[:4]
        return context


class CardListView(ListView):
    """The catalogue: 12 cards a page, with an optional name search."""

    template_name = "cards/card_list.html"
    context_object_name = "cards"
    paginate_by = 12

    def get_queryset(self):
        cards = Card.objects.select_related("card_set")
        self.query = self.request.GET.get("q", "").strip()
        if self.query:
            cards = cards.filter(name__icontains=self.query)
        return cards

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["query"] = self.query
        return context


class CardDetailView(DetailView):
    """One card, its reviews, and the add and review forms."""

    template_name = "cards/card_detail.html"
    context_object_name = "card"

    def get_queryset(self):
        return Card.objects.select_related("card_set")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        reviews = self.object.reviews.select_related("user")
        summary = reviews.aggregate(average=Avg("rating"), count=Count("id"))
        context["reviews"] = reviews
        context["rating"] = summary
        user = self.request.user
        if user.is_authenticated:
            entries = user.collection_entries.filter(card=self.object)
            context["my_entry"] = entries.first()
            context["my_review"] = reviews.filter(user=user).first()
            context["entry_form"] = CollectionEntryForm()
            context["review_form"] = ReviewForm()
        return context


class ReviewCreate(LoginMessageMixin, FormErrorMixin, CreateView):
    """Rate and review a card. Each user reviews a card once."""

    form_class = ReviewForm
    template_name = "cards/review_form.html"

    @cached_property
    def card(self):
        """The card named in the URL, or a 404 page."""
        return get_object_or_404(Card, pk=self.kwargs["card_pk"])

    def get(self, request, *args, **kwargs):
        return self.edit_if_reviewed() or super().get(request)

    def post(self, request, *args, **kwargs):
        return self.edit_if_reviewed() or super().post(request)

    def edit_if_reviewed(self):
        """Send a user who has already reviewed this card to edit it."""
        reviews = self.request.user.reviews.filter(card=self.card)
        review = reviews.first()
        if review is None:
            return None
        message = REVIEW_EXISTS.format(card=self.card.name)
        messages.info(self.request, message)
        return redirect("cards:edit_review", pk=review.pk)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["card"] = self.card
        return context

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.instance.card = self.card
        response = super().form_valid(form)
        messages.success(self.request, REVIEW_ADDED)
        return response

    def get_success_url(self):
        return reverse("cards:card_detail", args=[self.card.pk])


class OwnReviewMixin(LoginMessageMixin):
    """Limit a view to the logged-in user's reviews; others get a 404."""

    def get_queryset(self):
        return self.request.user.reviews.select_related("card")

    def get_success_url(self):
        return reverse("cards:card_detail", args=[self.object.card_id])


class ReviewEdit(OwnReviewMixin, FormErrorMixin, UpdateView):
    """Change the rating or text of your own review."""

    form_class = ReviewForm
    template_name = "cards/review_form.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["card"] = self.object.card
        return context

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, REVIEW_UPDATED)
        return response


class ReviewDelete(OwnReviewMixin, DeleteView):
    """Confirm, then delete your own review."""

    template_name = "cards/review_confirm_delete.html"
    context_object_name = "review"

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, REVIEW_DELETED)
        return response
