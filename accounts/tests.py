"""Tests for registering, logging in and logging out (US01 to US04)."""
from django.contrib.auth import get_user_model
from django.contrib.messages import get_messages
from django.test import TestCase
from django.urls import reverse

User = get_user_model()

STRONG_PASSWORD = "Vault-Pass-2026"


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
        }
        return self.client.post(reverse("account_signup"), data)

    def test_form_asks_for_username_and_both_passwords(self):
        response = self.client.get(reverse("account_signup"))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            list(response.context["form"].fields),
            ["username", "password1", "password2"],
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
