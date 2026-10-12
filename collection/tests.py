"""Tests for collection entries and the My Cards page."""
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.db import IntegrityError, transaction
from django.test import TestCase
from django.urls import reverse

from cards.models import Card, CardSet

from .models import CollectionEntry

User = get_user_model()


class CollectionEntryTests(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user("ash", password="Vault-Pass-2026")
        base_set = CardSet.objects.create(name="Base Set", quantity=102)
        cls.card = Card.objects.create(
            name="Blastoise", card_set=base_set, number=2,
            rarity=Card.Rarity.RARE_HOLO,
        )

    def test_defaults_to_one_owned_card(self):
        entry = CollectionEntry.objects.create(user=self.user, card=self.card)
        self.assertEqual(entry.status, CollectionEntry.Status.OWNED)
        self.assertEqual(entry.quantity, 1)
        self.assertEqual(entry.notes, "")

    def test_str(self):
        entry = CollectionEntry.objects.create(
            user=self.user, card=self.card, quantity=2,
            status=CollectionEntry.Status.WANTED,
        )
        self.assertEqual(str(entry), "ash: 2 x Blastoise (Wanted)")

    def test_one_entry_per_user_per_card_whatever_the_status(self):
        CollectionEntry.objects.create(user=self.user, card=self.card)
        with self.assertRaises(IntegrityError), transaction.atomic():
            CollectionEntry.objects.create(
                user=self.user, card=self.card,
                status=CollectionEntry.Status.WANTED,
            )

    def test_two_users_can_list_the_same_card(self):
        other = User.objects.create_user("misty", password="Vault-Pass-2026")
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

    def test_logged_out_visitor_is_sent_to_login(self):
        target = reverse("collection:my_cards")
        response = self.client.get(target)
        self.assertRedirects(
            response, f"{reverse('account_login')}?next={target}"
        )

    def test_user_sees_only_their_own_entries(self):
        ash = User.objects.create_user("ash", password="Vault-Pass-2026")
        misty = User.objects.create_user("misty", password="Vault-Pass-2026")
        base_set = CardSet.objects.create(name="Base Set", quantity=102)
        mine = Card.objects.create(
            name="Venusaur", card_set=base_set, number=15,
            rarity=Card.Rarity.RARE_HOLO,
        )
        theirs = Card.objects.create(
            name="Starmie", card_set=base_set, number=64,
            rarity=Card.Rarity.COMMON,
        )
        CollectionEntry.objects.create(user=ash, card=mine)
        CollectionEntry.objects.create(user=misty, card=theirs)
        self.client.force_login(ash)
        response = self.client.get(reverse("collection:my_cards"))
        self.assertContains(response, "Venusaur")
        self.assertNotContains(response, "Starmie")

    def test_empty_list_shows_a_message(self):
        user = User.objects.create_user("brock", password="Vault-Pass-2026")
        self.client.force_login(user)
        response = self.client.get(reverse("collection:my_cards"))
        self.assertContains(response, "Your cards list is empty.")
