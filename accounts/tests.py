"""Tests for accounts: register, log in and out, age check, deleting
an account, the information pages and security."""
from datetime import timedelta
from io import StringIO
from unittest import mock

from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.cache import cache
from django.core.management import call_command
from django.db import connection
from django.contrib.messages import get_messages
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from cards.models import Card, CardSet, Review
from collection.models import CollectionEntry

from .adapter import LOCKED, LOGIN_FAILED

COMMAND = "accounts.management.commands.clear_expired_cache"

User = get_user_model()

STRONG_PASSWORD = "Vault-Pass-2026"
ADULT_BIRTHDAY = "1995-06-15"


def message_texts(response):
    """Return the text of every message queued on a response."""
    return [str(m) for m in get_messages(response.wsgi_request)]


class RegisterTests(TestCase):
    """US01: register an account."""

    def register(self, username, password1, password2=None):
        if password2 is None:
            password2 = password1
        data = {
            "username": username,
            "password1": password1,
            "password2": password2,
            "date_of_birth": ADULT_BIRTHDAY,
        }
        return self.client.post(reverse("account_signup"), data)

    def test_form_asks_for_username_birthday_and_both_passwords(self):
        response = self.client.get(reverse("account_signup"))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            list(response.context["form"].fields),
            ["username", "date_of_birth", "password1", "password2"],
        )

    def test_valid_details_create_the_account_and_log_in(self):
        response = self.register("ash", STRONG_PASSWORD)
        self.assertRedirects(response, reverse("collection:my_cards"))
        self.assertTrue(User.objects.filter(username="ash").exists())
        self.assertEqual(
            message_texts(response),
            ["Your account has been created. Welcome to CardVault, ash!"],
        )
        self.assertTrue(response.wsgi_request.user.is_authenticated)

    def test_duplicate_username_is_rejected(self):
        User.objects.create_user("ash", password=STRONG_PASSWORD)
        response = self.register("ash", STRONG_PASSWORD)
        self.assertEqual(response.status_code, 200)
        self.assertFormError(
            response.context["form"], "username",
            "That username is already taken. Please choose another.",
        )
        self.assertEqual(User.objects.count(), 1)

    def test_short_password_is_rejected_naming_the_rule(self):
        response = self.register("ash", "Xy7!q")
        self.assertContains(response, "This password is too short.")
        self.assertFalse(User.objects.exists())

    def test_common_password_is_rejected_naming_the_rule(self):
        response = self.register("ash", "password123")
        self.assertContains(response, "This password is too common.")
        self.assertFalse(User.objects.exists())

    def test_numeric_password_is_rejected_naming_the_rule(self):
        response = self.register("ash", "8273645190")
        self.assertContains(response, "This password is entirely numeric.")
        self.assertFalse(User.objects.exists())

    def test_password_similar_to_username_is_rejected(self):
        response = self.register("pikachufan", "pikachufan1")
        self.assertContains(
            response, "The password is too similar to the username."
        )
        self.assertFalse(User.objects.exists())

    def test_mismatched_passwords_are_rejected(self):
        response = self.register("ash", STRONG_PASSWORD, "Different-Pass-1")
        self.assertFormError(
            response.context["form"], "password2",
            "You must type the same password each time.",
        )
        self.assertFalse(User.objects.exists())


class LoginTests(TestCase):
    """US02: log in."""

    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user("misty", password=STRONG_PASSWORD)

    def log_in(self, username, password, **extra):
        return self.client.post(
            reverse("account_login"),
            {"login": username, "password": password, **extra},
        )

    def test_valid_details_log_in_and_land_on_my_cards(self):
        response = self.log_in("misty", STRONG_PASSWORD)
        self.assertRedirects(response, reverse("collection:my_cards"))
        self.assertEqual(message_texts(response), ["Welcome back, misty!"])

    def test_login_returns_to_the_page_originally_requested(self):
        response = self.log_in("misty", STRONG_PASSWORD, next="/")
        self.assertRedirects(response, "/")

    def test_wrong_password_shows_one_generic_error(self):
        response = self.log_in("misty", "Wrong-Pass-2026")
        self.assertEqual(response.status_code, 200)
        self.assertFormError(
            response.context["form"], None,
            "Invalid username or password. Please try again.",
        )
        self.assertFalse(response.wsgi_request.user.is_authenticated)

    def test_unknown_username_shows_the_same_error(self):
        response = self.log_in("nobody", STRONG_PASSWORD)
        self.assertFormError(
            response.context["form"], None,
            "Invalid username or password. Please try again.",
        )

    def test_login_page_has_no_password_reset_link(self):
        response = self.client.get(reverse("account_login"))
        self.assertNotContains(response, "Forgot")


class LogoutTests(TestCase):
    """US03: log out."""

    def setUp(self):
        self.user = User.objects.create_user("brock", password=STRONG_PASSWORD)
        self.client.force_login(self.user)

    def test_post_logs_out_with_a_message(self):
        response = self.client.post(reverse("account_logout"))
        self.assertRedirects(response, reverse("home"))
        self.assertEqual(
            message_texts(response),
            ["You have been logged out. See you soon!"],
        )
        self.assertFalse(response.wsgi_request.user.is_authenticated)

    def test_logout_message_is_displayed_on_the_next_page(self):
        response = self.client.post(reverse("account_logout"), follow=True)
        self.assertContains(
            response, "You have been logged out. See you soon!"
        )
        self.assertContains(response, 'role="status"')

    def test_get_does_not_log_out(self):
        response = self.client.get(reverse("account_logout"))
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.wsgi_request.user.is_authenticated)

    def test_private_page_redirects_to_login_after_logout(self):
        self.client.post(reverse("account_logout"))
        target = reverse("collection:my_cards")
        response = self.client.get(target)
        self.assertRedirects(
            response, f"{reverse('account_login')}?next={target}"
        )


class NavigationTests(TestCase):
    """US04: see whether I am logged in."""

    def test_logged_out_navigation(self):
        response = self.client.get(reverse("home"))
        self.assertContains(response, reverse("account_login"))
        self.assertContains(response, reverse("account_signup"))
        self.assertNotContains(response, "Logged in as")
        self.assertNotContains(response, reverse("collection:my_cards"))

    def test_logged_in_navigation(self):
        user = User.objects.create_user("gary", password=STRONG_PASSWORD)
        self.client.force_login(user)
        response = self.client.get(reverse("home"))
        self.assertContains(response, "Logged in as <strong>gary</strong>")
        self.assertContains(response, reverse("collection:my_cards"))
        self.assertContains(response, "Log out")
        self.assertNotContains(response, reverse("account_signup"))


class SecurityHeaderTests(TestCase):
    """Every page carries the Content Security Policy headers."""

    def test_content_security_policy(self):
        response = self.client.get(reverse("home"))
        csp = response.headers["Content-Security-Policy"]
        self.assertIn("default-src 'self'", csp)
        self.assertIn("script-src 'self'", csp)
        self.assertIn("frame-ancestors 'none'", csp)
        self.assertNotIn("unsafe-inline", csp)

    def test_permissions_policy(self):
        response = self.client.get(reverse("home"))
        self.assertIn("camera=()", response.headers["Permissions-Policy"])

    def test_pages_cannot_be_framed(self):
        response = self.client.get(reverse("home"))
        self.assertEqual(response.headers["X-Frame-Options"], "DENY")

    def test_no_inline_scripts_in_the_page(self):
        response = self.client.get(reverse("home"))
        self.assertNotContains(response, "<script>")


class LoginRateLimitTests(TestCase):
    """django-allauth stops repeated password guessing."""

    url = reverse("account_login")
    wrong = {"login": "misty", "password": "Wrong-Pass-2026"}

    def setUp(self):
        User.objects.create_user("misty", password=STRONG_PASSWORD)

    def guess(self, data, address="203.0.113.1"):
        """Post a log in from one visitor's IP address, as Heroku's
        router reports it: the last entry of X-Forwarded-For."""
        forwarded = f"198.51.100.7, {address}"
        return self.client.post(self.url, data, HTTP_X_FORWARDED_FOR=forwarded)

    def test_third_wrong_password_is_an_ordinary_error(self):
        for _ in range(2):
            self.guess(self.wrong)
        response = self.guess(self.wrong)
        self.assertContains(response, LOGIN_FAILED)
        self.assertNotContains(response, "Too many failed log in attempts.")

    def test_fourth_wrong_password_is_blocked(self):
        for _ in range(3):
            self.guess(self.wrong)
        response = self.guess(self.wrong)
        self.assertContains(response, LOCKED)

    def test_correct_password_is_also_blocked_while_locked(self):
        for _ in range(3):
            self.guess(self.wrong)
        right = {"login": "misty", "password": STRONG_PASSWORD}
        response = self.guess(right)
        self.assertFalse(response.wsgi_request.user.is_authenticated)

    def test_lock_follows_the_username_across_ip_addresses(self):
        for number in range(1, 4):
            self.guess(self.wrong, address=f"203.0.113.{number}")
        response = self.guess(self.wrong, address="192.0.2.50")
        self.assertContains(response, LOCKED)

    def test_one_address_cannot_guess_across_many_usernames(self):
        for number in range(5):
            data = {"login": f"user{number}", "password": "Wrong-Pass-2026"}
            self.guess(data)
        right = {"login": "misty", "password": STRONG_PASSWORD}
        response = self.guess(right)
        self.assertContains(response, LOCKED)

    def test_other_visitors_can_still_log_in(self):
        for number in range(5):
            data = {"login": f"user{number}", "password": "Wrong-Pass-2026"}
            self.guess(data)
        right = {"login": "misty", "password": STRONG_PASSWORD}
        response = self.guess(right, address="192.0.2.50")
        self.assertTrue(response.wsgi_request.user.is_authenticated)

    def test_changing_the_first_forwarded_address_does_not_help(self):
        for number in range(5):
            data = {"login": f"user{number}", "password": "Wrong-Pass-2026"}
            forwarded = f"10.0.0.{number}, 203.0.113.1"
            self.client.post(self.url, data, HTTP_X_FORWARDED_FOR=forwarded)
        right = {"login": "misty", "password": STRONG_PASSWORD}
        response = self.guess(right)
        self.assertContains(response, LOCKED)


class SignupRateLimitTests(TestCase):
    """One IP address can register at most 10 accounts an hour."""

    def test_eleventh_registration_gets_the_too_many_attempts_page(self):
        url = reverse("account_signup")
        for number in range(10):
            data = {
                "username": f"trainer{number}",
                "date_of_birth": ADULT_BIRTHDAY,
                "password1": STRONG_PASSWORD,
                "password2": STRONG_PASSWORD,
            }
            self.client.post(url, data)
            self.client.post(reverse("account_logout"))
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 429)
        self.assertTemplateUsed(response, "429.html")
        self.assertContains(response, "Too many attempts", status_code=429)


class ClearExpiredCacheTests(TestCase):
    """Expired rate limit notes are deleted from the database."""

    def test_deletes_expired_entries_and_keeps_current_ones(self):
        cache.set("old-note", 1, 60)
        cache.set("current-note", 1, 3600)
        later = timezone.now() + timedelta(minutes=5)
        with mock.patch(f"{COMMAND}.timezone.now", return_value=later):
            call_command("clear_expired_cache", stdout=StringIO())
        with connection.cursor() as cursor:
            cursor.execute("SELECT cache_key FROM cardvault_cache")
            keys = [row[0] for row in cursor.fetchall()]
        self.assertFalse(any(key.endswith("old-note") for key in keys))
        self.assertTrue(any(key.endswith("current-note") for key in keys))


class DatabaseSettingsTests(TestCase):
    """Database connections are checked and slow queries stopped."""

    def test_slow_queries_are_stopped_after_10_seconds(self):
        database = settings.DATABASES["default"]
        self.assertTrue(database["CONN_HEALTH_CHECKS"])
        with connection.cursor() as cursor:
            cursor.execute("SHOW statement_timeout")
            self.assertEqual(cursor.fetchone()[0], "10s")


class AdminLoginTests(TestCase):
    """The Django admin's log in goes through django-allauth."""

    def test_logged_out_visitor_is_sent_to_the_normal_log_in(self):
        response = self.client.get(reverse("admin:login"))
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.url.startswith(reverse("account_login")))

    def test_admin_password_form_cannot_be_used(self):
        User.objects.create_superuser("boss", password=STRONG_PASSWORD)
        data = {"username": "boss", "password": STRONG_PASSWORD}
        response = self.client.post(reverse("admin:login"), data)
        self.assertEqual(response.status_code, 302)
        self.assertNotIn("_auth_user_id", self.client.session)

    def test_superusers_go_on_to_the_admin(self):
        boss = User.objects.create_superuser("boss", password=STRONG_PASSWORD)
        self.client.force_login(boss)
        response = self.client.get(reverse("admin:login"))
        self.assertRedirects(response, reverse("admin:index"))

    def test_superusers_can_open_the_admin(self):
        boss = User.objects.create_superuser("boss", password=STRONG_PASSWORD)
        self.client.force_login(boss)
        response = self.client.get(reverse("admin:index"))
        self.assertEqual(response.status_code, 200)

    def test_ordinary_users_are_refused(self):
        user = User.objects.create_user("ash", password=STRONG_PASSWORD)
        self.client.force_login(user)
        response = self.client.get(reverse("admin:login"))
        self.assertEqual(response.status_code, 403)

    def test_staff_who_are_not_superusers_are_refused(self):
        staff = User.objects.create_user(
            "helper", password=STRONG_PASSWORD, is_staff=True
        )
        self.client.force_login(staff)
        response = self.client.get(reverse("admin:index"), follow=True)
        self.assertEqual(response.status_code, 403)
        self.assertTemplateUsed(response, "403.html")

    def test_unsafe_next_address_is_ignored(self):
        boss = User.objects.create_superuser("boss", password=STRONG_PASSWORD)
        self.client.force_login(boss)
        url = reverse("admin:login") + "?next=https://evil.example/"
        response = self.client.get(url)
        self.assertRedirects(response, reverse("admin:index"))


class AdminSiteTests(TestCase):
    """US28: the admin is CardVault's own, with the right models."""

    @classmethod
    def setUpTestData(cls):
        cls.boss = User.objects.create_superuser(
            "boss", password=STRONG_PASSWORD
        )
        base = CardSet.objects.create(name="Base Set", quantity=102)
        cls.card = Card.objects.create(
            name="Charizzard", card_set=base, number=4,
            rarity=Card.Rarity.RARE_HOLO,
        )

    def setUp(self):
        self.client.force_login(self.boss)

    def test_admin_is_titled_for_cardvault(self):
        response = self.client.get(reverse("admin:index"))
        self.assertContains(response, "CardVault administration")
        self.assertContains(response, "Manage CardVault")

    def test_models_are_listed_without_email_addresses(self):
        response = self.client.get(reverse("admin:index"))
        models = [
            "Card sets", "Cards", "Reviews", "Collection entries",
            "Contact messages", "Users",
        ]
        for model in models:
            self.assertContains(response, model)
        self.assertNotContains(response, "Email addresses")

    def test_cards_can_be_searched_by_set(self):
        url = reverse("admin:cards_card_changelist") + "?q=base"
        response = self.client.get(url)
        self.assertContains(response, "Charizzard")

    def test_a_wrong_card_detail_can_be_corrected(self):
        url = reverse("admin:cards_card_change", args=[self.card.pk])
        data = {
            "name": "Charizard",
            "card_set": self.card.card_set.pk,
            "number": 4,
            "rarity": Card.Rarity.RARE_HOLO,
            "image_url": "https://images.pokemontcg.io/base1/4.png",
        }
        response = self.client.post(url, data)
        self.assertRedirects(response, reverse("admin:cards_card_changelist"))
        self.card.refresh_from_db()
        self.assertEqual(self.card.name, "Charizard")

    def test_card_page_shows_a_picture_preview(self):
        self.card.image_url = "https://images.pokemontcg.io/base1/4.png"
        self.card.save()
        url = reverse("admin:cards_card_change", args=[self.card.pk])
        response = self.client.get(url)
        self.assertContains(response, 'src="https://images.pokemontcg.io/')


class AdminLinkTests(TestCase):
    """US28: an Admin link in the header, for superusers only."""

    def test_superusers_see_the_admin_link(self):
        boss = User.objects.create_superuser("boss", password=STRONG_PASSWORD)
        self.client.force_login(boss)
        response = self.client.get(reverse("home"))
        link = f'<a href="{reverse("admin:index")}">Admin</a>'
        self.assertContains(response, link, html=True)

    def test_ordinary_users_and_visitors_do_not(self):
        admin_url = f'href="{reverse("admin:index")}"'
        response = self.client.get(reverse("home"))
        self.assertNotContains(response, admin_url)
        user = User.objects.create_user("ash", password=STRONG_PASSWORD)
        self.client.force_login(user)
        response = self.client.get(reverse("home"))
        self.assertNotContains(response, admin_url)


def years_ago(years, days=0):
    """A date of birth exactly `years` years ago, plus `days` days."""
    today = timezone.localdate()
    try:
        born = today.replace(year=today.year - years)
    except ValueError:
        born = today.replace(year=today.year - years, day=28)
    return (born + timedelta(days=days)).isoformat()


class AgeCheckTests(TestCase):
    """US29: you must be 13 or older to register."""

    def register(self, date_of_birth, username="newbie"):
        data = {
            "username": username,
            "date_of_birth": date_of_birth,
            "password1": STRONG_PASSWORD,
            "password2": STRONG_PASSWORD,
        }
        return self.client.post(reverse("account_signup"), data)

    def test_thirteenth_birthday_today_can_register(self):
        response = self.register(years_ago(13))
        self.assertRedirects(response, reverse("collection:my_cards"))
        self.assertTrue(User.objects.filter(username="newbie").exists())

    def test_one_day_short_of_thirteen_is_refused(self):
        response = self.register(years_ago(13, days=1))
        self.assertRedirects(response, reverse("account_signup"))
        self.assertFalse(User.objects.exists())

    def test_registration_stays_closed_after_an_under_age_attempt(self):
        self.register(years_ago(10))
        response = self.client.get(reverse("account_signup"))
        self.assertContains(response, "you need to be 13 or older")
        self.assertNotContains(response, 'name="password1"')
        response = self.register(ADULT_BIRTHDAY, username="liar")
        self.assertFalse(User.objects.exists())

    def test_date_in_the_future_is_rejected(self):
        response = self.register(years_ago(-1))
        self.assertFormError(
            response.context["form"], "date_of_birth",
            "Please enter your real date of birth.",
        )
        self.assertFalse(User.objects.exists())

    def test_date_of_birth_is_required(self):
        response = self.register("")
        self.assertIn("date_of_birth", response.context["form"].errors)
        self.assertFalse(User.objects.exists())

    def test_date_of_birth_is_not_stored(self):
        self.register(ADULT_BIRTHDAY)
        field_names = [f.name for f in User._meta.get_fields()]
        self.assertNotIn("date_of_birth", field_names)


class DeleteAccountTests(TestCase):
    """US30: delete my account and everything in it."""

    def setUp(self):
        self.user = User.objects.create_user("ash", password=STRONG_PASSWORD)
        self.other = User.objects.create_user(
            "misty", password=STRONG_PASSWORD
        )
        card_set = CardSet.objects.create(name="Set", quantity=1)
        self.card = Card.objects.create(
            name="Pikachu", card_set=card_set, number=58,
            rarity=Card.Rarity.COMMON,
        )
        for user in (self.user, self.other):
            CollectionEntry.objects.create(user=user, card=self.card)
            Review.objects.create(
                user=user, card=self.card, rating=5, body="Great"
            )
        self.url = reverse("delete_account")

    def test_logged_out_visitor_is_asked_to_log_in(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.url.startswith(reverse("account_login")))

    def test_page_lists_what_will_be_deleted(self):
        self.client.force_login(self.user)
        response = self.client.get(self.url)
        self.assertContains(response, "the 1 card on your My Cards list")
        self.assertContains(response, "the 1 review you have written")

    def test_wrong_password_deletes_nothing(self):
        self.client.force_login(self.user)
        data = {"password": "Wrong-Pass-2026"}
        response = self.client.post(self.url, data)
        self.assertFormError(
            response.context["form"], "password",
            "That password is not correct.",
        )
        self.assertTrue(User.objects.filter(pk=self.user.pk).exists())

    def test_correct_password_deletes_account_cards_and_reviews(self):
        self.client.force_login(self.user)
        response = self.client.post(self.url, {"password": STRONG_PASSWORD})
        self.assertRedirects(response, reverse("home"))
        self.assertFalse(User.objects.filter(pk=self.user.pk).exists())
        self.assertFalse(CollectionEntry.objects.filter(user_id=self.user.pk))
        self.assertFalse(Review.objects.filter(user_id=self.user.pk))
        expected = ["Your account, cards and reviews have been deleted."]
        self.assertEqual(message_texts(response), expected)
        self.assertFalse(response.wsgi_request.user.is_authenticated)

    def test_other_users_and_the_card_are_untouched(self):
        self.client.force_login(self.user)
        self.client.post(self.url, {"password": STRONG_PASSWORD})
        self.assertTrue(User.objects.filter(pk=self.other.pk).exists())
        self.assertEqual(CollectionEntry.objects.count(), 1)
        self.assertEqual(Review.objects.count(), 1)
        self.assertTrue(Card.objects.filter(pk=self.card.pk).exists())


class PrivacyAndAccessibilityPageTests(TestCase):
    """US31 and US32: the information pages, linked from every page."""

    def test_pages_load_and_are_linked_in_the_footer(self):
        home = self.client.get(reverse("home"))
        for name in ("privacy", "accessibility"):
            with self.subTest(page=name):
                response = self.client.get(reverse(name))
                self.assertEqual(response.status_code, 200)
                self.assertContains(home, reverse(name))

    def test_privacy_page_lists_both_cookies(self):
        response = self.client.get(reverse("privacy"))
        self.assertContains(response, "sessionid")
        self.assertContains(response, "csrftoken")

    def test_privacy_page_lists_what_is_stored_in_the_browser(self):
        response = self.client.get(reverse("privacy"))
        self.assertContains(response, "cardvault-theme")
        self.assertContains(response, "cardvault-intro-seen")

    def test_favicon_ico_redirects_to_the_icon(self):
        response = self.client.get("/favicon.ico")
        self.assertRedirects(
            response, "/static/images/favicon.ico",
            fetch_redirect_response=False,
        )

    def test_delete_link_only_shown_when_logged_in(self):
        delete_url = reverse("delete_account")
        response = self.client.get(reverse("home"))
        self.assertNotContains(response, delete_url)
        user = User.objects.create_user("ash", password=STRONG_PASSWORD)
        self.client.force_login(user)
        response = self.client.get(reverse("home"))
        self.assertContains(response, delete_url)

    def test_messages_do_not_set_their_own_cookie(self):
        User.objects.create_user("misty", password=STRONG_PASSWORD)
        data = {"login": "misty", "password": STRONG_PASSWORD}
        response = self.client.post(reverse("account_login"), data)
        self.assertNotIn("messages", response.cookies)


class UsernameRuleTests(TestCase):
    """Usernames are public, so an email address cannot be one."""

    def test_email_address_username_is_refused(self):
        data = {
            "username": "someone@example.com",
            "date_of_birth": ADULT_BIRTHDAY,
            "password1": STRONG_PASSWORD,
            "password2": STRONG_PASSWORD,
        }
        response = self.client.post(reverse("account_signup"), data)
        self.assertContains(response, "shown publicly next to your reviews")
        self.assertFalse(User.objects.exists())
