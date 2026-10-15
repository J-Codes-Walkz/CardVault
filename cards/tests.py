"""Tests for the catalogue: models, fixtures, pages and reviews."""
from datetime import timedelta

from django.contrib.auth import get_user_model
from django.contrib.messages import get_messages
from django.core.exceptions import ValidationError
from django.core.management import call_command
from django.db import IntegrityError, transaction
from django.db.models import ProtectedError
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from .models import Card, CardSet, Review
from .templatetags.card_extras import stars

User = get_user_model()
PASSWORD = "Vault-Pass-2026"


def message_texts(response):
    """Return the text of every message queued on a response."""
    return [str(m) for m in get_messages(response.wsgi_request)]


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

    def test_image_is_optional(self):
        self.card.full_clean()
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
        base_set = CardSet.objects.create(name="Base Set", quantity=102)
        cls.card = make_card(base_set)

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


class StarsFilterTests(TestCase):

    def test_whole_rating(self):
        self.assertEqual(stars(4), "★★★★☆")

    def test_average_is_rounded(self):
        self.assertEqual(stars(4.6), "★★★★★")

    def test_no_rating_shows_empty_stars(self):
        self.assertEqual(stars(None), "☆☆☆☆☆")


class TesterFixtureTests(TestCase):
    """The AAA, BBB and CCC tester cards used for front-end testing."""

    def test_fixture_loads_three_tester_cards(self):
        call_command("loaddata", "tester_cards", verbosity=0)
        names = list(Card.objects.values_list("name", flat=True))
        self.assertEqual(names, ["AAA", "BBB", "CCC"])
        self.assertEqual(CardSet.objects.get().name, "Tester Set")

    def test_loading_twice_does_not_duplicate(self):
        call_command("loaddata", "tester_cards", verbosity=0)
        call_command("loaddata", "tester_cards", verbosity=0)
        self.assertEqual(Card.objects.count(), 3)


class ReviewEditedTests(TestCase):

    def test_new_review_is_not_marked_edited(self):
        user = User.objects.create_user("ash", password=PASSWORD)
        card = make_card(CardSet.objects.create(name="Set", quantity=1))
        review = Review.objects.create(
            user=user, card=card, rating=4, body="Nice."
        )
        self.assertFalse(review.is_edited)

    def test_review_changed_later_is_marked_edited(self):
        user = User.objects.create_user("ash", password=PASSWORD)
        card = make_card(CardSet.objects.create(name="Set", quantity=1))
        review = Review.objects.create(
            user=user, card=card, rating=4, body="Nice."
        )
        an_hour_ago = timezone.now() - timedelta(hours=1)
        Review.objects.filter(pk=review.pk).update(created_at=an_hour_ago)
        review.refresh_from_db()
        review.save()
        self.assertTrue(review.is_edited)


class CatalogueTests(TestCase):
    """US07 and US08: browse and search the catalogue."""

    @classmethod
    def setUpTestData(cls):
        card_set = CardSet.objects.create(name="Tester Set", quantity=13)
        for number in range(1, 14):
            make_card(card_set, number=number, name=f"Card {number:02d}")
        make_card(card_set, number=99, name="Charizard")

    def test_twelve_cards_per_page(self):
        response = self.client.get(reverse("cards:card_list"))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context["cards"]), 12)
        response = self.client.get(reverse("cards:card_list") + "?page=2")
        self.assertEqual(len(response.context["cards"]), 2)

    def test_each_tile_links_to_the_card(self):
        card = Card.objects.get(name="Charizard")
        response = self.client.get(reverse("cards:card_list") + "?page=2")
        self.assertContains(response, card.get_absolute_url())

    def test_missing_image_shows_placeholder_with_alt_text(self):
        response = self.client.get(reverse("cards:card_list"))
        self.assertContains(response, "card-placeholder.svg")
        self.assertContains(response, 'alt="Card 01: no image yet"')

    def test_search_is_partial_and_case_insensitive(self):
        response = self.client.get(reverse("cards:card_list") + "?q=CHAR")
        names = [card.name for card in response.context["cards"]]
        self.assertEqual(names, ["Charizard"])
        self.assertContains(response, '1 card found for "CHAR"')

    def test_search_with_no_match(self):
        response = self.client.get(reverse("cards:card_list") + "?q=zzz")
        self.assertContains(response, 'No cards match "zzz".')
        self.assertContains(response, "Try a different name, set or rarity.")

    def test_search_term_is_kept_in_pagination_links(self):
        response = self.client.get(reverse("cards:card_list") + "?q=card")
        self.assertContains(response, "?q=card&amp;page=2")


class CardDetailTests(TestCase):
    """US10 and US21: a card's page and its reviews."""

    @classmethod
    def setUpTestData(cls):
        cls.ash = User.objects.create_user("ash", password=PASSWORD)
        cls.misty = User.objects.create_user("misty", password=PASSWORD)
        cls.card = make_card(CardSet.objects.create(name="Set", quantity=1))
        cls.url = cls.card.get_absolute_url()

    def test_logged_out_visitor_sees_details_and_login_prompts(self):
        response = self.client.get(self.url)
        self.assertContains(response, "Charizard")
        self.assertNotContains(response, "price")
        self.assertContains(response, "Log in to add this card")
        self.assertContains(response, "Log in to write a review")
        self.assertNotIn("entry_form", response.context)

    def test_logged_in_user_sees_both_forms(self):
        self.client.force_login(self.ash)
        response = self.client.get(self.url)
        self.assertContains(response, "Add to My Cards")
        self.assertContains(response, "Submit review")

    def test_unknown_card_is_404(self):
        response = self.client.get(reverse("cards:card_detail", args=[999]))
        self.assertEqual(response.status_code, 404)

    def test_no_reviews_message(self):
        response = self.client.get(self.url)
        self.assertContains(response, "No reviews yet. Be the first")

    def test_average_rating_and_count(self):
        Review.objects.create(
            user=self.ash, card=self.card, rating=5, body="Great"
        )
        Review.objects.create(
            user=self.misty, card=self.card, rating=2, body="Meh"
        )
        response = self.client.get(self.url)
        self.assertContains(response, "Average 3.5 out of 5 from 2 reviews")

    def test_edit_and_delete_only_on_own_review(self):
        mine = Review.objects.create(
            user=self.ash, card=self.card, rating=5, body="Mine"
        )
        theirs = Review.objects.create(
            user=self.misty, card=self.card, rating=3, body="Theirs"
        )
        self.client.force_login(self.ash)
        response = self.client.get(self.url)
        mine_url = reverse("cards:edit_review", args=[mine.pk])
        theirs_url = reverse("cards:edit_review", args=[theirs.pk])
        self.assertContains(response, mine_url)
        self.assertNotContains(response, theirs_url)
        self.assertNotContains(response, "Submit review")


class ReviewCrudTests(TestCase):
    """US18, US19 and US20: write, edit and delete a review."""

    @classmethod
    def setUpTestData(cls):
        cls.ash = User.objects.create_user("ash", password=PASSWORD)
        cls.misty = User.objects.create_user("misty", password=PASSWORD)
        cls.card = make_card(CardSet.objects.create(name="Set", quantity=1))
        cls.add_url = reverse("cards:add_review", args=[cls.card.pk])

    def setUp(self):
        self.client.force_login(self.ash)

    def make_review(self, user=None):
        return Review.objects.create(
            user=user or self.ash, card=self.card, rating=3, body="Original"
        )

    def test_submit_review(self):
        data = {"rating": 4, "body": "Lovely art."}
        response = self.client.post(self.add_url, data)
        self.assertRedirects(response, self.card.get_absolute_url())
        review = Review.objects.get()
        self.assertEqual((review.user, review.rating), (self.ash, 4))
        expected = ["Thank you for submitting your review!"]
        self.assertEqual(message_texts(response), expected)

    def test_rating_and_text_are_required(self):
        response = self.client.post(self.add_url, {})
        self.assertEqual(response.status_code, 200)
        form = response.context["form"]
        self.assertIn("rating", form.errors)
        self.assertIn("body", form.errors)
        expected = ["Please correct the errors below and try again."]
        self.assertEqual(message_texts(response), expected)
        self.assertFalse(Review.objects.exists())

    def test_rating_above_5_is_rejected(self):
        response = self.client.post(self.add_url, {"rating": 6, "body": "x"})
        self.assertIn("rating", response.context["form"].errors)
        self.assertFalse(Review.objects.exists())

    def test_second_review_redirects_to_edit_the_first(self):
        review = self.make_review()
        data = {"rating": 1, "body": "Again"}
        response = self.client.post(self.add_url, data)
        edit_url = reverse("cards:edit_review", args=[review.pk])
        self.assertRedirects(response, edit_url)
        self.assertEqual(Review.objects.count(), 1)
        self.assertIn("You have already reviewed", message_texts(response)[0])

    def test_logged_out_visitor_is_asked_to_log_in(self):
        self.client.logout()
        response = self.client.post(self.add_url, {"rating": 5, "body": "x"})
        login = reverse("account_login")
        self.assertRedirects(response, f"{login}?next={self.add_url}")
        expected = ["Please log in to view that page."]
        self.assertEqual(message_texts(response), expected)
        self.assertFalse(Review.objects.exists())

    def test_edit_own_review(self):
        review = self.make_review()
        url = reverse("cards:edit_review", args=[review.pk])
        response = self.client.post(url, {"rating": 5, "body": "Changed"})
        self.assertRedirects(response, self.card.get_absolute_url())
        review.refresh_from_db()
        self.assertEqual((review.rating, review.body), (5, "Changed"))
        expected = ["Your review was updated successfully."]
        self.assertEqual(message_texts(response), expected)

    def test_cannot_edit_another_users_review(self):
        review = self.make_review(user=self.misty)
        url = reverse("cards:edit_review", args=[review.pk])
        self.assertEqual(self.client.get(url).status_code, 404)
        response = self.client.post(url, {"rating": 1, "body": "Hacked"})
        self.assertEqual(response.status_code, 404)
        review.refresh_from_db()
        self.assertEqual(review.body, "Original")

    def test_delete_asks_for_confirmation(self):
        review = self.make_review()
        url = reverse("cards:delete_review", args=[review.pk])
        response = self.client.get(url)
        self.assertContains(response, "Delete your review of Charizard?")
        self.assertTrue(Review.objects.exists())

    def test_delete_own_review(self):
        review = self.make_review()
        url = reverse("cards:delete_review", args=[review.pk])
        response = self.client.post(url)
        self.assertRedirects(response, self.card.get_absolute_url())
        self.assertFalse(Review.objects.exists())
        self.assertEqual(message_texts(response), ["Your review was deleted."])

    def test_cannot_delete_another_users_review(self):
        review = self.make_review(user=self.misty)
        url = reverse("cards:delete_review", args=[review.pk])
        self.assertEqual(self.client.post(url).status_code, 404)
        self.assertTrue(Review.objects.filter(pk=review.pk).exists())


class HomePageTests(TestCase):
    """US06: the purpose is clear and featured cards are shown."""

    def test_featured_cards_are_shown(self):
        call_command("loaddata", "tester_cards", verbosity=0)
        response = self.client.get(reverse("home"))
        self.assertContains(response, "Featured cards")
        for name in ("AAA", "BBB", "CCC"):
            self.assertContains(response, name)

    def test_logged_out_calls_to_action(self):
        response = self.client.get(reverse("home"))
        self.assertContains(response, "Create account")
        self.assertContains(response, "Browse cards")


class BaseSetCardsFixtureTests(TestCase):
    """US27: the 102 Base Set cards built once from the Pokémon TCG API."""

    def load(self):
        call_command("loaddata", "pokemon_cardsets", verbosity=0)
        call_command("loaddata", "base_set_cards", verbosity=0)

    def test_all_102_cards_load_into_the_base_set(self):
        self.load()
        base_set = CardSet.objects.get(name="Base Set")
        self.assertEqual(base_set.cards.count(), 102)
        self.assertEqual(base_set.cards.count(), base_set.quantity)

    def test_card_details_match_the_printed_set(self):
        self.load()
        charizard = Card.objects.get(card_set__name="Base Set", number=4)
        self.assertEqual(charizard.name, "Charizard")
        self.assertEqual(charizard.rarity, Card.Rarity.RARE_HOLO)
        self.assertTrue(charizard.image_url.startswith("https://images."))

    def test_loading_twice_does_not_duplicate(self):
        self.load()
        self.load()
        self.assertEqual(Card.objects.count(), 102)

    def test_tester_cards_are_kept_alongside(self):
        call_command("loaddata", "tester_cards", verbosity=0)
        self.load()
        self.assertEqual(Card.objects.count(), 105)
        names = Card.objects.filter(pk__lte=3).values_list("name", flat=True)
        self.assertEqual(list(names), ["AAA", "BBB", "CCC"])


class ImageFallbackTests(TestCase):
    """Linked card pictures fall back to the placeholder if they fail."""

    def test_linked_pictures_name_the_placeholder_fallback(self):
        card_set = CardSet.objects.create(name="Set", quantity=1)
        card = make_card(card_set)
        card.image_url = "https://images.pokemontcg.io/base1/4.png"
        card.save()
        fallback = 'data-fallback="/static/images/card-placeholder.svg"'
        for url in (reverse("cards:card_list"), card.get_absolute_url()):
            with self.subTest(url=url):
                self.assertContains(self.client.get(url), fallback)

    def test_fallback_script_loads_in_the_head(self):
        response = self.client.get(reverse("home"))
        head = response.content.decode().split("</head>")[0]
        self.assertIn("js/image-fallback.js", head)


class SearchAndFilterTests(TestCase):
    """US08 and US09: search by name, set or rarity, and filter."""

    @classmethod
    def setUpTestData(cls):
        base = CardSet.objects.create(name="Base Set", quantity=102)
        jungle = CardSet.objects.create(name="Jungle", quantity=64)
        cls.jungle = jungle
        rarity = Card.Rarity
        cards = [
            ("Charizard", base, 4, rarity.RARE_HOLO),
            ("Raichu", base, 14, rarity.RARE_HOLO),
            ("Electabuzz", base, 20, rarity.RARE),
            ("Charmeleon", base, 24, rarity.UNCOMMON),
            ("Charmander", base, 46, rarity.COMMON),
            ("Jolteon", jungle, 4, rarity.RARE_HOLO),
        ]
        for name, card_set, number, card_rarity in cards:
            Card.objects.create(
                name=name, card_set=card_set, number=number,
                rarity=card_rarity,
            )

    def names(self, query_string):
        url = reverse("cards:card_list") + query_string
        response = self.client.get(url)
        return sorted(card.name for card in response.context["cards"])

    def test_rarity_words_in_either_order(self):
        holos = ["Charizard", "Jolteon", "Raichu"]
        for query in ("holo", "holo rare", "Rare Holo", "holos"):
            with self.subTest(query=query):
                self.assertEqual(self.names(f"?q={query}"), holos)

    def test_common_does_not_match_uncommon(self):
        self.assertEqual(self.names("?q=common"), ["Charmander"])

    def test_words_combine_name_set_and_rarity(self):
        self.assertEqual(self.names("?q=char+holo"), ["Charizard"])
        self.assertEqual(self.names("?q=jungle"), ["Jolteon"])

    def test_rarity_filter(self):
        self.assertEqual(self.names("?rarity=RARE"), ["Electabuzz"])

    def test_set_filter(self):
        query = f"?set={self.jungle.pk}"
        self.assertEqual(self.names(query), ["Jolteon"])

    def test_search_and_filters_combine(self):
        query = f"?q=holo&set={self.jungle.pk}&rarity=RARE_HOLO"
        self.assertEqual(self.names(query), ["Jolteon"])

    def test_unknown_filter_values_are_ignored(self):
        self.assertEqual(len(self.names("?rarity=SHINY&set=abc")), 6)

    def test_dropdowns_keep_the_chosen_values(self):
        url = reverse("cards:card_list") + "?rarity=RARE"
        response = self.client.get(url)
        self.assertContains(response, '<option value="RARE" selected>')

    def test_filters_are_kept_in_pagination_links(self):
        base = CardSet.objects.get(name="Base Set")
        for number in range(50, 63):
            Card.objects.create(
                name=f"Filler {number}", card_set=base, number=number,
                rarity=Card.Rarity.COMMON,
            )
        url = reverse("cards:card_list") + "?rarity=COMMON"
        response = self.client.get(url)
        self.assertContains(response, "?rarity=COMMON&amp;page=2")

    def test_clear_link_shown_only_when_filtering(self):
        clear = "Clear search and filters"
        url = reverse("cards:card_list")
        self.assertNotContains(self.client.get(url), clear)
        self.assertContains(self.client.get(url + "?rarity=RARE"), clear)
