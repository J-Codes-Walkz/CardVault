"""Tests for the site-wide error pages (US25) and error logging."""
from unittest import mock

from django.conf import settings
from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse

User = get_user_model()
PASSWORD = "Vault-Pass-2026"
HOME_VIEW = "cards.views.HomeView.get_context_data"


class NotFoundPageTests(TestCase):

    def test_unknown_address_shows_the_404_page(self):
        response = self.client.get("/no-such-page/")
        self.assertEqual(response.status_code, 404)
        self.assertTemplateUsed(response, "404.html")
        text = "We couldn't find that page"
        self.assertContains(response, text, status_code=404)

    def test_404_page_links_home_and_offers_a_search(self):
        response = self.client.get("/no-such-page/")
        home = f'href="{reverse("home")}"'
        self.assertContains(response, home, status_code=404)
        search = f'action="{reverse("cards:card_list")}"'
        self.assertContains(response, search, status_code=404)

    def test_unknown_card_shows_the_404_page(self):
        response = self.client.get(reverse("cards:card_detail", args=[99999]))
        self.assertTemplateUsed(response, "404.html")

    def test_404_page_keeps_the_logged_in_header(self):
        User.objects.create_user("ash", password=PASSWORD)
        self.client.login(username="ash", password=PASSWORD)
        response = self.client.get("/no-such-page/")
        self.assertContains(response, "Logged in as", status_code=404)

    def test_404_page_shows_no_technical_details(self):
        response = self.client.get("/no-such-page/")
        self.assertNotContains(response, "Traceback", status_code=404)
        self.assertNotContains(response, "urlpatterns", status_code=404)


class PermissionDeniedPageTests(TestCase):

    def test_non_staff_user_opening_the_admin_sees_the_403_page(self):
        User.objects.create_user("ash", password=PASSWORD)
        self.client.login(username="ash", password=PASSWORD)
        response = self.client.get(reverse("admin:login"))
        self.assertEqual(response.status_code, 403)
        self.assertTemplateUsed(response, "403.html")
        text = "You don't have permission to see this page"
        self.assertContains(response, text, status_code=403)


class FormExpiredPageTests(TestCase):

    def test_form_sent_without_a_valid_csrf_token(self):
        client = Client(enforce_csrf_checks=True)
        data = {"login": "ash", "password": PASSWORD}
        response = client.post(reverse("account_login"), data)
        self.assertEqual(response.status_code, 403)
        self.assertTemplateUsed(response, "403_csrf.html")
        self.assertContains(response, "This form has expired", status_code=403)


class BadRequestPageTests(TestCase):

    def test_unknown_host_shows_the_400_page(self):
        response = self.client.get("/", HTTP_HOST="evil.example")
        self.assertEqual(response.status_code, 400)
        self.assertTemplateUsed(response, "400.html")


class ServerErrorPageTests(TestCase):

    def setUp(self):
        self.client.raise_request_exception = False

    def crash(self):
        """Load the home page with its view made to fail."""
        with mock.patch(HOME_VIEW, side_effect=RuntimeError("Test crash")):
            with self.assertLogs("django.request", level="ERROR") as logs:
                response = self.client.get(reverse("home"))
        return response, logs

    def test_a_crash_shows_the_500_page(self):
        response, _ = self.crash()
        self.assertEqual(response.status_code, 500)
        self.assertTemplateUsed(response, "500.html")
        text = "Something went wrong on our side"
        self.assertContains(response, text, status_code=500)

    def test_500_page_shows_no_technical_details(self):
        response, _ = self.crash()
        self.assertNotContains(response, "Test crash", status_code=500)
        self.assertNotContains(response, "Traceback", status_code=500)

    def test_crash_is_written_to_the_logs_with_its_traceback(self):
        _, logs = self.crash()
        self.assertIn("Test crash", logs.output[0])
        self.assertIn("Traceback", logs.output[0])

    def test_500_page_uses_no_template_tags(self):
        path = settings.BASE_DIR / "templates" / "500.html"
        with open(path, encoding="utf-8") as page:
            source = page.read()
        self.assertNotIn("{%", source)
        self.assertNotIn("{{", source)
