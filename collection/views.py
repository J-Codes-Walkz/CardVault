"""Views for a user's own cards: list, add, edit and remove."""
from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse
from django.utils.functional import cached_property
from django.views.generic import CreateView, DeleteView, ListView, UpdateView

from accounts.mixins import FormErrorMixin, LoginMessageMixin
from cards.models import Card

from .forms import CollectionEntryForm
from .models import CollectionEntry

ENTRY_ADDED = "{card} was added to your cards."
ENTRY_EXISTS = "You already have {card} on your list. "
ENTRY_EXISTS += "Edit that entry to change it."
ENTRY_UPDATED = "Your entry for {card} was updated."
ENTRY_REMOVED = "{card} was removed from your cards."

STATUS_TABS = {
    "owned": CollectionEntry.Status.OWNED,
    "wanted": CollectionEntry.Status.WANTED,
}


class MyCardsView(LoginMessageMixin, ListView):
    """The logged-in user's own entries, newest first, by status tab."""

    template_name = "collection/my_cards.html"
    context_object_name = "entries"

    def get_queryset(self):
        entries = self.request.user.collection_entries
        entries = entries.select_related("card", "card__card_set")
        self.tab = self.request.GET.get("status", "all")
        if self.tab in STATUS_TABS:
            entries = entries.filter(status=STATUS_TABS[self.tab])
        else:
            self.tab = "all"
        return entries

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["tab"] = self.tab
        context["has_any"] = self.request.user.collection_entries.exists()
        return context


class OwnEntryMixin(LoginMessageMixin):
    """Limit a view to the logged-in user's entries; others get a 404."""

    def get_queryset(self):
        return self.request.user.collection_entries.select_related("card")

    def get_success_url(self):
        return reverse("collection:my_cards")


class EntryCreate(LoginMessageMixin, FormErrorMixin, CreateView):
    """Add a card from the catalogue to My Cards, as owned or wanted."""

    form_class = CollectionEntryForm
    template_name = "collection/entry_form.html"

    @cached_property
    def card(self):
        """The card named in the URL, or a 404 page."""
        return get_object_or_404(Card, pk=self.kwargs["card_pk"])

    def get(self, request, *args, **kwargs):
        return self.edit_if_listed() or super().get(request)

    def post(self, request, *args, **kwargs):
        return self.edit_if_listed() or super().post(request)

    def edit_if_listed(self):
        """Send a user who already lists this card to edit that entry."""
        entries = self.request.user.collection_entries.filter(card=self.card)
        entry = entries.first()
        if entry is None:
            return None
        messages.error(self.request, ENTRY_EXISTS.format(card=self.card.name))
        return redirect("collection:edit_entry", pk=entry.pk)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["card"] = self.card
        return context

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.instance.card = self.card
        response = super().form_valid(form)
        messages.success(self.request, ENTRY_ADDED.format(card=self.card.name))
        return response

    def get_success_url(self):
        return reverse("collection:my_cards")


class EntryEdit(OwnEntryMixin, FormErrorMixin, UpdateView):
    """Change the status, quantity or notes of your own entry."""

    form_class = CollectionEntryForm
    template_name = "collection/entry_form.html"
    context_object_name = "entry"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["card"] = self.object.card
        return context

    def form_valid(self, form):
        response = super().form_valid(form)
        card = self.object.card.name
        messages.success(self.request, ENTRY_UPDATED.format(card=card))
        return response


class EntryDelete(OwnEntryMixin, DeleteView):
    """Confirm, then remove your own entry. The card itself stays."""

    template_name = "collection/entry_confirm_delete.html"
    context_object_name = "entry"

    def form_valid(self, form):
        card = self.object.card.name
        response = super().form_valid(form)
        messages.success(self.request, ENTRY_REMOVED.format(card=card))
        return response
