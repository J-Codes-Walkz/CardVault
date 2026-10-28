"""Tests for the Contact page and the Home and Contact links."""
from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.messages import get_messages
from django.core.cache import cache
from django.test import RequestFactory, TestCase
from django.urls import reverse

from .models import ContactMessage
from .views import MESSAGE_LIMIT, THANK_YOU, TOO_MANY, visitor_key

User = get_user_model()
PASSWORD = "Vault-Pass-2026"
CONTACT_URL = reverse("contact:contact")
VALID = {"name": "Ash", "email": "ash@example.com", "message": "Hello!"}


def message_texts(response):
    """Return the text of every message queued on a response."""
    return [str(m) for m in get_messages(response.wsgi_request)]


class ContactMessageModelTests(TestCase):

    def test_str_and_defaults(self):
        message = ContactMessage.objects.create(**VALID)
        self.assertFalse(message.handled)
        self.assertTrue(str(message).startswith("Ash ("))

    def test_newest_first(self):
        first = ContactMessage.objects.create(**VALID)
        second = ContactMessage.objects.create(**VALID)
        self.assertEqual(list(ContactMessage.objects.all()), [second, first])


class ContactPageTests(TestCase):

    def setUp(self):
        cache.clear()

    def test_page_loads_for_anyone(self):
        response = self.client.get(CONTACT_URL)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "contact/contact.html")
        self.assertContains(response, 'name="name"')
        self.assertContains(response, 'name="email"')
        self.assertContains(response, 'name="message"')

    def test_trap_field_is_hidden_and_skipped_by_tab(self):
        response = self.client.get(CONTACT_URL)
        self.assertContains(response, 'class="field trap"')
        self.assertContains(response, 'tabindex="-1"')

    def test_name_is_filled_in_for_logged_in_users(self):
        User.objects.create_user("ash", password=PASSWORD)
        self.client.login(username="ash", password=PASSWORD)
        response = self.client.get(CONTACT_URL)
        self.assertEqual(response.context["form"].initial["name"], "ash")

    def test_valid_message_is_saved_with_a_thank_you(self):
        response = self.client.post(CONTACT_URL, VALID, follow=True)
        self.assertRedirects(response, reverse("home"))
        self.assertEqual(ContactMessage.objects.count(), 1)
        saved = ContactMessage.objects.get()
        self.assertEqual(saved.email, "ash@example.com")
        self.assertEqual(message_texts(response), [THANK_YOU])
        self.assertContains(response, "check your junk or spam folder")

    def test_bad_email_is_refused(self):
        data = dict(VALID, email="not-an-email")
        response = self.client.post(CONTACT_URL, data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(ContactMessage.objects.count(), 0)
        self.assertContains(response, "Please correct the errors below")

    def test_every_field_is_required(self):
        response = self.client.post(CONTACT_URL, {})
        self.assertEqual(response.context["form"].errors.keys(), set(VALID))
        self.assertEqual(ContactMessage.objects.count(), 0)

    def test_message_over_2000_characters_is_refused(self):
        data = dict(VALID, message="x" * 2001)
        self.client.post(CONTACT_URL, data)
        self.assertEqual(ContactMessage.objects.count(), 0)

    def test_bot_filling_the_trap_is_thanked_but_not_saved(self):
        data = dict(VALID, website="http://spam.example")
        response = self.client.post(CONTACT_URL, data, follow=True)
        self.assertEqual(ContactMessage.objects.count(), 0)
        self.assertEqual(message_texts(response), [THANK_YOU])

    def test_sixth_message_in_an_hour_is_refused(self):
        for _ in range(MESSAGE_LIMIT):
            self.client.post(CONTACT_URL, VALID)
        response = self.client.post(CONTACT_URL, VALID)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(ContactMessage.objects.count(), MESSAGE_LIMIT)
        self.assertIn(TOO_MANY, message_texts(response))

    def test_limit_is_per_visitor(self):
        for _ in range(MESSAGE_LIMIT):
            self.client.post(CONTACT_URL, VALID)
        other = {"HTTP_X_FORWARDED_FOR": "203.0.113.9"}
        self.client.post(CONTACT_URL, VALID, **other)
        self.assertEqual(ContactMessage.objects.count(), MESSAGE_LIMIT + 1)


class VisitorKeyTests(TestCase):

    def test_uses_the_address_heroku_added_last(self):
        factory = RequestFactory()
        spoofed = "1.2.3.4, 203.0.113.9"
        request = factory.get("/", HTTP_X_FORWARDED_FOR=spoofed)
        real = factory.get("/", HTTP_X_FORWARDED_FOR="203.0.113.9")
        self.assertEqual(visitor_key(request), visitor_key(real))

    def test_address_is_never_stored_as_it_is(self):
        request = RequestFactory().get("/", REMOTE_ADDR="203.0.113.9")
        self.assertNotIn("203.0.113.9", visitor_key(request))


class ContactAdminTests(TestCase):

    def test_registered_with_message_read_only(self):
        model_admin = admin.site._registry[ContactMessage]
        self.assertIn("message", model_admin.readonly_fields)
        self.assertIn("email", model_admin.readonly_fields)
        self.assertEqual(model_admin.list_editable, ("handled",))

    def test_messages_cannot_be_added_in_the_admin(self):
        boss = User.objects.create_superuser("boss", password=PASSWORD)
        self.client.force_login(boss)
        response = self.client.get(reverse("admin:contact_contactmessage_add"))
        self.assertEqual(response.status_code, 403)


class NavigationTests(TestCase):

    def test_home_and_contact_links_on_every_page(self):
        for url in (reverse("home"), reverse("cards:card_list"), CONTACT_URL):
            response = self.client.get(url)
            self.assertContains(response, f'href="{reverse("home")}"')
            self.assertContains(response, f'href="{CONTACT_URL}"')

    def test_current_page_is_marked(self):
        response = self.client.get(CONTACT_URL)
        link = f'<a href="{CONTACT_URL}" aria-current="page">Contact</a>'
        self.assertContains(response, link, html=True)
        response = self.client.get(reverse("home"))
        home = reverse("home")
        link = f'<a href="{home}" aria-current="page">Home</a>'
        self.assertContains(response, link, html=True)

    def test_logged_in_users_see_contact_too(self):
        User.objects.create_user("ash", password=PASSWORD)
        self.client.login(username="ash", password=PASSWORD)
        response = self.client.get(reverse("home"))
        self.assertContains(response, ">Contact</a>")

    def test_privacy_page_explains_the_contact_form(self):
        response = self.client.get(reverse("privacy"))
        self.assertContains(response, "If you contact us")
        self.assertContains(response, f'href="{CONTACT_URL}"')
