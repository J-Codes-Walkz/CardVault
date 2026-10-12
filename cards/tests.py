"""Tests for the catalogue models and the Base Set fixture."""
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.core.management import call_command
from django.db import IntegrityError, transaction
from django.db.models import ProtectedError
from django.test import TestCase

from .models import Card, CardSet, Review

User = get_user_model()


def make_card(card_set, number=4, name="Charizard"):
    return Card.objects.create(
        name=name,
        card_set=card_set,
        number=number,
        rarity=Card.Rarity.RARE_HOLO,
    )


class CardSetTests(TestCase):

    def test_str_is_the_set_name(self):
        card_set = CardSet.objects.create(name="Base Set", quantity=102)
        self.assertEqual(str(card_set), "Base Set")

    def test_set_names_are_unique(self):
        CardSet.objects.create(name="Base Set", quantity=102)
        with self.assertRaises(IntegrityError), transaction.atomic():
            CardSet.objects.create(name="Base Set", quantity=102)


class CardTests(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.base_set = CardSet.objects.create(name="Base Set", quantity=102)
        cls.card = make_card(cls.base_set)

    def test_str_names_the_card_set_and_number(self):
        self.assertEqual(str(self.card), "Charizard (Base Set #4)")

    def test_price_and_image_are_optional(self):
        self.card.full_clean()
        self.assertIsNone(self.card.market_price)
        self.assertEqual(self.card.image_url, "")

    def test_number_is_unique_within_a_set(self):
        with self.assertRaises(IntegrityError), transaction.atomic():
            make_card(self.base_set, number=4, name="Duplicate")

    def test_same_number_is_allowed_in_another_set(self):
        jungle = CardSet.objects.create(name="Jungle", quantity=64)
        make_card(jungle, number=4, name="Jolteon")
        self.assertEqual(Card.objects.filter(number=4).count(), 2)

    def test_unknown_rarity_fails_validation(self):
        self.card.rarity = "SHINY"
        with self.assertRaises(ValidationError):
            self.card.full_clean()

    def test_a_set_with_cards_cannot_be_deleted(self):
        with self.assertRaises(ProtectedError):
            self.base_set.delete()


class ReviewTests(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user("ash", password="Vault-Pass-2026")
        cls.card = make_card(CardSet.objects.create(name="Base Set",
                                                    quantity=102))

    def review(self, rating=5, user=None):
        return Review(
            user=user or self.user, card=self.card, rating=rating,
            body="A classic.",
        )

    def test_str(self):
        review = self.review()
        review.save()
        self.assertEqual(str(review), "ash rated Charizard 5/5")

    def test_one_review_per_user_per_card(self):
        self.review().save()
        with self.assertRaises(IntegrityError), transaction.atomic():
            self.review(rating=3).save()

    def test_two_users_can_review_the_same_card(self):
        other = User.objects.create_user("misty", password="Vault-Pass-2026")
        self.review().save()
        self.review(user=other).save()
        self.assertEqual(self.card.reviews.count(), 2)

    def test_rating_outside_1_to_5_fails_validation(self):
        for rating in (0, 6):
            with self.subTest(rating=rating):
                with self.assertRaises(ValidationError):
                    self.review(rating=rating).full_clean()

    def test_database_rejects_rating_outside_1_to_5(self):
        for rating in (0, 6):
            with self.subTest(rating=rating):
                with self.assertRaises(IntegrityError), transaction.atomic():
                    self.review(rating=rating).save()

    def test_deleting_the_user_deletes_their_reviews(self):
        self.review().save()
        self.user.delete()
        self.assertFalse(Review.objects.exists())


class BaseSetFixtureTests(TestCase):
    """US27: the fixture seeds the catalogue and is safe to re-run."""

    def test_fixture_loads_base_set(self):
        call_command("loaddata", "pokemon_cardsets", verbosity=0)
        base_set = CardSet.objects.get(name="Base Set")
        self.assertEqual(base_set.quantity, 102)

    def test_loading_twice_does_not_duplicate(self):
        call_command("loaddata", "pokemon_cardsets", verbosity=0)
        call_command("loaddata", "pokemon_cardsets", verbosity=0)
        self.assertEqual(CardSet.objects.count(), 1)
