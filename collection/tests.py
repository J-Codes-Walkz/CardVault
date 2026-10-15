"""Tests for collection entries and the My Cards pages."""
from django.contrib.auth import get_user_model
from django.contrib.messages import get_messages
from django.core.exceptions import ValidationError
from django.db import IntegrityError, transaction
from django.test import TestCase
from django.urls import reverse

from cards.models import Card, CardSet, Review

from .models import CollectionEntry

User = get_user_model()
PASSWORD = "Vault-Pass-2026"
OWNED = CollectionEntry.Status.OWNED
WANTED = CollectionEntry.Status.WANTED


def message_texts(response):
    """Return the text of every message queued on a response."""
    return [str(m) for m in get_messages(response.wsgi_request)]


def make_card(name="Blastoise", number=2):
    card_set, _ = CardSet.objects.get_or_create(name="Set", quantity=102)
    rarity = Card.Rarity.RARE_HOLO
    return Card.objects.create(
        name=name, card_set=card_set, number=number, rarity=rarity
    )


class CollectionEntryTests(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user("ash", password=PASSWORD)
        cls.card = make_card()

    def test_defaults_to_one_owned_card(self):
        entry = CollectionEntry.objects.create(user=self.user, card=self.card)
        self.assertEqual(entry.status, OWNED)
        self.assertEqual(entry.quantity, 1)
        self.assertEqual(entry.notes, "")

    def test_str(self):
        entry = CollectionEntry.objects.create(
            user=self.user, card=self.card, quantity=2, status=WANTED
        )
        self.assertEqual(str(entry), "ash: 2 x Blastoise (Wanted)")

    def test_one_entry_per_user_per_card_whatever_the_status(self):
        CollectionEntry.objects.create(user=self.user, card=self.card)
        with self.assertRaises(IntegrityError), transaction.atomic():
            CollectionEntry.objects.create(
                user=self.user, card=self.card, status=WANTED
            )

    def test_two_users_can_list_the_same_card(self):
        other = User.objects.create_user("misty", password=PASSWORD)
        CollectionEntry.objects.create(user=self.user, card=self.card)
        CollectionEntry.objects.create(user=other, card=self.card)
        self.assertEqual(self.card.collection_entries.count(), 2)

    def test_quantity_of_zero_fails_validation(self):
        entry = CollectionEntry(user=self.user, card=self.card, quantity=0)
        with self.assertRaises(ValidationError):
            entry.full_clean()

    def test_database_rejects_quantity_of_zero(self):
        with self.assertRaises(IntegrityError), transaction.atomic():
            CollectionEntry.objects.create(
                user=self.user, card=self.card, quantity=0
            )

    def test_deleting_an_entry_keeps_the_card(self):
        entry = CollectionEntry.objects.create(user=self.user, card=self.card)
        entry.delete()
        self.assertTrue(Card.objects.filter(pk=self.card.pk).exists())


class MyCardsViewTests(TestCase):
    """US12: view my cards, and US05: only mine."""

    @classmethod
    def setUpTestData(cls):
        cls.ash = User.objects.create_user("ash", password=PASSWORD)
        cls.misty = User.objects.create_user("misty", password=PASSWORD)
        cls.url = reverse("collection:my_cards")
        venusaur = make_card("Venusaur", 15)
        starmie = make_card("Starmie", 64)
        pikachu = make_card("Pikachu", 58)
        CollectionEntry.objects.create(user=cls.ash, card=venusaur)
        CollectionEntry.objects.create(
            user=cls.ash, card=pikachu, status=WANTED
        )
        CollectionEntry.objects.create(user=cls.misty, card=starmie)

    def test_logged_out_visitor_is_sent_to_login_with_a_message(self):
        response = self.client.get(self.url)
        login = reverse("account_login")
        self.assertRedirects(response, f"{login}?next={self.url}")
        expected = ["Please log in to view that page."]
        self.assertEqual(message_texts(response), expected)

    def test_user_sees_only_their_own_entries(self):
        self.client.force_login(self.ash)
        response = self.client.get(self.url)
        self.assertContains(response, "Venusaur")
        self.assertContains(response, "Pikachu")
        self.assertNotContains(response, "Starmie")

    def test_owned_tab(self):
        self.client.force_login(self.ash)
        response = self.client.get(self.url + "?status=owned")
        self.assertContains(response, "Venusaur")
        self.assertNotContains(response, "Pikachu")

    def test_wanted_tab(self):
        self.client.force_login(self.ash)
        response = self.client.get(self.url + "?status=wanted")
        self.assertContains(response, "Pikachu")
        self.assertNotContains(response, "Venusaur")

    def test_unknown_tab_shows_all(self):
        self.client.force_login(self.ash)
        response = self.client.get(self.url + "?status=nonsense")
        self.assertEqual(len(response.context["entries"]), 2)

    def test_every_entry_has_edit_and_remove(self):
        self.client.force_login(self.ash)
        response = self.client.get(self.url)
        for entry in self.ash.collection_entries.all():
            edit = reverse("collection:edit_entry", args=[entry.pk])
            remove = reverse("collection:delete_entry", args=[entry.pk])
            self.assertContains(response, edit)
            self.assertContains(response, remove)

    def test_empty_list_message(self):
        brock = User.objects.create_user("brock", password=PASSWORD)
        self.client.force_login(brock)
        response = self.client.get(self.url)
        self.assertContains(response, "Your cards list is empty.")

    def test_empty_tab_message(self):
        self.client.force_login(self.misty)
        response = self.client.get(self.url + "?status=wanted")
        self.assertContains(response, "You have no wanted cards yet.")


class EntryCreateTests(TestCase):
    """US11: add a card to My Cards."""

    @classmethod
    def setUpTestData(cls):
        cls.ash = User.objects.create_user("ash", password=PASSWORD)
        cls.card = make_card()
        cls.url = reverse("collection:add_entry", args=[cls.card.pk])

    def setUp(self):
        self.client.force_login(self.ash)

    def test_add_card_as_owned_with_quantity(self):
        data = {"status": OWNED, "quantity": 2, "notes": "Shadowless"}
        response = self.client.post(self.url, data)
        self.assertRedirects(response, reverse("collection:my_cards"))
        entry = CollectionEntry.objects.get()
        self.assertEqual((entry.user, entry.card), (self.ash, self.card))
        self.assertEqual((entry.status, entry.quantity), (OWNED, 2))
        expected = ["Blastoise was added to your cards."]
        self.assertEqual(message_texts(response), expected)

    def test_add_card_as_wanted(self):
        data = {"status": WANTED, "quantity": 1, "notes": ""}
        self.client.post(self.url, data)
        self.assertEqual(CollectionEntry.objects.get().status, WANTED)

    def test_quantity_of_zero_is_rejected(self):
        data = {"status": OWNED, "quantity": 0, "notes": ""}
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, 200)
        self.assertIn("quantity", response.context["form"].errors)
        expected = ["Please correct the errors below and try again."]
        self.assertEqual(message_texts(response), expected)
        self.assertFalse(CollectionEntry.objects.exists())

    def test_duplicate_goes_to_the_existing_entry(self):
        entry = CollectionEntry.objects.create(user=self.ash, card=self.card)
        data = {"status": WANTED, "quantity": 5, "notes": ""}
        response = self.client.post(self.url, data)
        edit_url = reverse("collection:edit_entry", args=[entry.pk])
        self.assertRedirects(response, edit_url)
        self.assertEqual(CollectionEntry.objects.count(), 1)
        text = "You already have Blastoise on your list. "
        text += "Edit that entry to change it."
        self.assertEqual(message_texts(response), [text])

    def test_unknown_card_is_404(self):
        url = reverse("collection:add_entry", args=[999])
        data = {"status": OWNED, "quantity": 1, "notes": ""}
        self.assertEqual(self.client.post(url, data).status_code, 404)

    def test_logged_out_visitor_cannot_add(self):
        self.client.logout()
        data = {"status": OWNED, "quantity": 1, "notes": ""}
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, 302)
        self.assertFalse(CollectionEntry.objects.exists())


class EntryEditTests(TestCase):
    """US13: edit a card entry, and US05: only my own."""

    @classmethod
    def setUpTestData(cls):
        cls.ash = User.objects.create_user("ash", password=PASSWORD)
        cls.misty = User.objects.create_user("misty", password=PASSWORD)
        cls.card = make_card()

    def setUp(self):
        self.client.force_login(self.ash)
        self.entry = CollectionEntry.objects.create(
            user=self.ash, card=self.card, quantity=1
        )
        self.url = reverse("collection:edit_entry", args=[self.entry.pk])

    def test_form_is_prefilled(self):
        response = self.client.get(self.url)
        self.assertEqual(response.context["form"].instance, self.entry)
        self.assertContains(response, "Edit your entry for Blastoise")

    def test_change_status_quantity_and_notes(self):
        data = {"status": WANTED, "quantity": 3, "notes": "Trade"}
        response = self.client.post(self.url, data)
        self.assertRedirects(response, reverse("collection:my_cards"))
        self.entry.refresh_from_db()
        self.assertEqual(self.entry.status, WANTED)
        self.assertEqual(self.entry.quantity, 3)
        self.assertEqual(self.entry.notes, "Trade")
        expected = ["Your entry for Blastoise was updated."]
        self.assertEqual(message_texts(response), expected)

    def test_quantity_below_one_is_rejected(self):
        data = {"status": OWNED, "quantity": 0, "notes": ""}
        response = self.client.post(self.url, data)
        self.assertIn("quantity", response.context["form"].errors)
        self.entry.refresh_from_db()
        self.assertEqual(self.entry.quantity, 1)

    def test_cannot_edit_another_users_entry(self):
        theirs = CollectionEntry.objects.create(
            user=self.misty, card=self.card, quantity=1
        )
        url = reverse("collection:edit_entry", args=[theirs.pk])
        self.assertEqual(self.client.get(url).status_code, 404)
        data = {"status": WANTED, "quantity": 9, "notes": "Hacked"}
        self.assertEqual(self.client.post(url, data).status_code, 404)
        theirs.refresh_from_db()
        self.assertEqual(theirs.quantity, 1)


class EntryDeleteTests(TestCase):
    """US14: remove a card from My Cards, and US05: only my own."""

    @classmethod
    def setUpTestData(cls):
        cls.ash = User.objects.create_user("ash", password=PASSWORD)
        cls.misty = User.objects.create_user("misty", password=PASSWORD)
        cls.card = make_card()

    def setUp(self):
        self.client.force_login(self.ash)
        self.entry = CollectionEntry.objects.create(
            user=self.ash, card=self.card
        )
        self.url = reverse("collection:delete_entry", args=[self.entry.pk])

    def test_confirmation_page_names_the_card(self):
        response = self.client.get(self.url)
        self.assertContains(response, "Remove Blastoise from My Cards?")
        self.assertTrue(CollectionEntry.objects.exists())

    def test_confirming_removes_the_entry_but_keeps_the_card(self):
        response = self.client.post(self.url)
        self.assertRedirects(response, reverse("collection:my_cards"))
        self.assertFalse(CollectionEntry.objects.exists())
        self.assertTrue(Card.objects.filter(pk=self.card.pk).exists())
        expected = ["Blastoise was removed from your cards."]
        self.assertEqual(message_texts(response), expected)

    def test_cancel_link_returns_to_my_cards(self):
        response = self.client.get(self.url)
        self.assertContains(response, reverse("collection:my_cards"))

    def test_cannot_remove_another_users_entry(self):
        theirs = CollectionEntry.objects.create(
            user=self.misty, card=self.card
        )
        url = reverse("collection:delete_entry", args=[theirs.pk])
        self.assertEqual(self.client.post(url).status_code, 404)
        self.assertTrue(CollectionEntry.objects.filter(pk=theirs.pk).exists())


class MyCardsRatingTests(TestCase):
    """My Cards shows my own star rating, or a Rate it link."""

    @classmethod
    def setUpTestData(cls):
        cls.ash = User.objects.create_user("ash", password=PASSWORD)
        cls.misty = User.objects.create_user("misty", password=PASSWORD)
        cls.rated = make_card("Raichu", 14)
        cls.unrated = make_card("Pikachu", 58)
        for card in (cls.rated, cls.unrated):
            CollectionEntry.objects.create(
                user=cls.ash, card=card, notes="Bought at a car boot sale"
            )
        Review.objects.create(
            user=cls.ash, card=cls.rated, rating=4, body="Great"
        )
        Review.objects.create(
            user=cls.misty, card=cls.unrated, rating=1, body="Meh"
        )

    def setUp(self):
        self.client.force_login(self.ash)
        self.response = self.client.get(reverse("collection:my_cards"))

    def test_my_rating_shows_as_stars(self):
        self.assertContains(self.response, "★★★★☆")
        self.assertContains(self.response, "4 out of 5 stars for Raichu")

    def test_unrated_card_offers_rate_it(self):
        url = reverse("cards:add_review", args=[self.unrated.pk])
        self.assertContains(self.response, f'href="{url}"')

    def test_other_users_ratings_are_not_shown_as_mine(self):
        self.assertNotContains(self.response, "★☆☆☆☆")

    def test_notes_show_as_a_preview(self):
        self.assertContains(self.response, "entry-note-preview")
        self.assertContains(self.response, "Bought at a car boot sale")

    def test_ratings_are_read_in_one_query(self):
        url = reverse("collection:my_cards")
        # Session, user, entries with ratings, and "has any entries":
        # the same 4 queries however many cards are on the list.
        with self.assertNumQueries(4):
            self.client.get(url)
