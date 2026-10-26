"""Views for a user's own cards: list, add, edit, got it and remove."""
from django.contrib import messages
from django.db.models import Count, OuterRef, Q, Subquery, Sum
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse
from django.utils.functional import cached_property
from django.utils.http import urlencode
from django.views.generic import CreateView, DeleteView, ListView, UpdateView

from accounts.mixins import FormErrorMixin, LoginMessageMixin
from cards.models import Card, CardSet, Review

from .forms import CollectionEntryForm, GotItForm
from .models import CollectionEntry

ENTRY_ADDED = "{card} was added to your cards."
ENTRY_EXISTS = "You already have {card} on your list. "
ENTRY_EXISTS += "Edit that entry to change it."
ENTRY_UPDATED = "Your entry for {card} was updated."
ENTRY_REMOVED = "{card} was removed from your cards."
GOT_IT = "{card} moved to your collection."

OWNED = CollectionEntry.Status.OWNED
WANTED = CollectionEntry.Status.WANTED
STATUS_TABS = {"owned": OWNED, "wanted": WANTED}
TAB_LABELS = {"all": "All", "owned": "Owned", "wanted": "Wanted"}

# The only orders My Cards can be sorted in: anything else in the
# address is ignored, so it can never reach the database.
SORTS = {
    "newest": ("Newest first", ["-created_at"]),
    "oldest": ("Oldest first", ["created_at"]),
    "name": ("Name, A to Z", ["card__name", "card__card_set__name"]),
    "set": ("Set and card number", ["card__card_set__name", "card__number"]),
}
DEFAULT_SORT = "newest"


class MyCardsView(LoginMessageMixin, ListView):
    """The logged-in user's own entries, newest first, by status tab."""

    template_name = "collection/my_cards.html"
    context_object_name = "entries"

    def get_queryset(self):
        entries = self.request.user.collection_entries
        entries = entries.select_related("card", "card__card_set")
        # The user's own star rating for each card, if they have
        # reviewed it, read alongside the entries in the same query.
        my_reviews = Review.objects.filter(
            user=OuterRef("user"), card=OuterRef("card")
        )
        my_rating = Subquery(my_reviews.values("rating")[:1])
        entries = entries.annotate(my_rating=my_rating)
        self.tab = self.request.GET.get("status", "all")
        if self.tab in STATUS_TABS:
            entries = entries.filter(status=STATUS_TABS[self.tab])
        else:
            self.tab = "all"
        self.set_id = self.request.GET.get("set", "")
        if self.set_id.isdigit():
            entries = entries.filter(card__card_set_id=self.set_id)
        else:
            self.set_id = ""
        self.sort = self.request.GET.get("sort", DEFAULT_SORT)
        if self.sort not in SORTS:
            self.sort = DEFAULT_SORT
        return entries.order_by(*SORTS[self.sort][1])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        totals = self.totals(user)
        context["totals"] = totals
        context["has_any"] = totals["owned_cards"] + totals["wanted_cards"]
        sets = CardSet.objects.filter(cards__collection_entries__user=user)
        context["card_sets"] = sets.distinct()
        context["sorts"] = [(key, label) for key, (label, _) in SORTS.items()]
        context["sort"] = self.sort
        context["set_id"] = self.set_id
        context["tab"] = self.tab
        context["tabs"] = self.tab_links()
        return context

    def totals(self, user):
        """US15: copies owned, different cards owned and cards wanted,
        counted in one query. Wanted cards are not in the owned totals."""
        owned = Q(status=OWNED)
        return user.collection_entries.aggregate(
            owned_total=Sum("quantity", filter=owned, default=0),
            owned_cards=Count("pk", filter=owned),
            wanted_cards=Count("pk", filter=Q(status=WANTED)),
        )

    def tab_links(self):
        """The All, Owned and Wanted tabs, each keeping the chosen sort
        and set, so switching tab does not undo them."""
        keep = {}
        if self.sort != DEFAULT_SORT:
            keep["sort"] = self.sort
        if self.set_id:
            keep["set"] = self.set_id
        url = reverse("collection:my_cards")
        tabs = []
        for key, label in TAB_LABELS.items():
            query = dict(keep, status=key) if key != "all" else keep
            link = f"{url}?{urlencode(query)}" if query else url
            current = key == self.tab
            tabs.append({"label": label, "url": link, "current": current})
        return tabs


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


class EntryGotIt(OwnEntryMixin, FormErrorMixin, UpdateView):
    """US17: move one of your Wanted cards to Owned, confirming how
    many you got. Owned entries, and other users' entries, are 404."""

    form_class = GotItForm
    template_name = "collection/got_it.html"
    context_object_name = "entry"

    def get_queryset(self):
        return super().get_queryset().filter(status=WANTED)

    def form_valid(self, form):
        form.instance.status = OWNED
        response = super().form_valid(form)
        card = self.object.card.name
        messages.success(self.request, GOT_IT.format(card=card))
        return response

    def get_success_url(self):
        return reverse("collection:my_cards") + "?status=owned"


class EntryDelete(OwnEntryMixin, DeleteView):
    """Confirm, then remove your own entry. The card itself stays."""

    template_name = "collection/entry_confirm_delete.html"
    context_object_name = "entry"

    def form_valid(self, form):
        card = self.object.card.name
        response = super().form_valid(form)
        messages.success(self.request, ENTRY_REMOVED.format(card=card))
        return response
