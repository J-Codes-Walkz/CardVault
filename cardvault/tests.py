"""Tests for the site-wide error pages (US25) and error logging."""
import re
from unittest import mock

from django.conf import settings
from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse

User = get_user_model()
PASSWORD = "Vault-Pass-2026"
HOME_VIEW = "cards.views.HomeView.get_context_data"


class NotFoundPageTests(TestCase):
    """The 404 page (US25)."""

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
    """The 403 page (US25)."""

    def test_non_staff_user_opening_the_admin_sees_the_403_page(self):
        User.objects.create_user("ash", password=PASSWORD)
        self.client.login(username="ash", password=PASSWORD)
        response = self.client.get(reverse("admin:login"))
        self.assertEqual(response.status_code, 403)
        self.assertTemplateUsed(response, "403.html")
        text = "You don't have permission to see this page"
        self.assertContains(response, text, status_code=403)


class FormExpiredPageTests(TestCase):
    """The "This form has expired" page shown when a CSRF check fails."""

    def test_form_sent_without_a_valid_csrf_token(self):
        client = Client(enforce_csrf_checks=True)
        data = {"login": "ash", "password": PASSWORD}
        response = client.post(reverse("account_login"), data)
        self.assertEqual(response.status_code, 403)
        self.assertTemplateUsed(response, "403_csrf.html")
        self.assertContains(response, "This form has expired", status_code=403)


class BadRequestPageTests(TestCase):
    """The 400 page (US25)."""

    def test_unknown_host_shows_the_400_page(self):
        response = self.client.get("/", HTTP_HOST="evil.example")
        self.assertEqual(response.status_code, 400)
        self.assertTemplateUsed(response, "400.html")


class ServerErrorPageTests(TestCase):
    """The 500 page, and that crashes are logged with their traceback."""

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


class ExternalLinkTests(TestCase):
    """Links to other sites open in a new tab, and say so."""

    FOLDERS = ["templates", "accounts", "cards", "collection", "contact"]
    EXTERNAL = re.compile(r'<a\s[^>]*href="https?://[^>]*>.*?</a>', re.S)

    def external_links(self):
        """Yield every external link in every template's source."""
        for folder in self.FOLDERS:
            for path in (settings.BASE_DIR / folder).rglob("*.html"):
                source = path.read_text(encoding="utf-8")
                for link in self.EXTERNAL.findall(source):
                    yield path.name, link

    def test_template_links_open_safely_in_a_new_tab_and_say_so(self):
        links = list(self.external_links())
        self.assertEqual(len(links), 5)
        for name, link in links:
            with self.subTest(name, link=link):
                self.assertIn('target="_blank"', link)
                self.assertIn('rel="noopener noreferrer"', link)
                self.assertIn("(opens in a new tab)", link)

    def test_privacy_page_shows_the_new_tab_links(self):
        response = self.client.get(reverse("privacy"))
        self.assertContains(response, 'target="_blank"', count=2)
