"""The Contact page."""
import hashlib

from allauth.account.adapter import get_adapter
from django.contrib import messages
from django.core.cache import cache
from django.shortcuts import redirect
from django.views.generic import FormView

from accounts.mixins import FormErrorMixin

from .forms import ContactForm

THANK_YOU = "Thank you for your enquiry. We aim to reply within 2 to 3 days. "
THANK_YOU += "If nothing arrives in your inbox, please check your junk or "
THANK_YOU += "spam folder."
TOO_MANY = "You have sent several messages recently. Please try again later."
# Each visitor may send 5 messages an hour.
MESSAGE_LIMIT = 5
LIMIT_SECONDS = 60 * 60


def visitor_key(request):
    """A cache key for the visitor's IP address, hashed so the address
    itself is never stored. The address is found the same way as for
    the log in limits (see ALLAUTH_TRUSTED_PROXY_COUNT in settings)."""
    address = get_adapter(request).get_client_ip(request)
    digest = hashlib.sha256(address.encode()).hexdigest()
    return f"contact-sent:{digest}"


class ContactView(FormErrorMixin, FormView):
    """Send CardVault a message; it is saved for the admin to answer."""

    form_class = ContactForm
    template_name = "contact/contact.html"

    def get_initial(self):
        initial = super().get_initial()
        if self.request.user.is_authenticated:
            initial["name"] = self.request.user.username
        return initial

    def form_valid(self, form):
        key = visitor_key(self.request)
        sent = cache.get(key, 0)
        if sent >= MESSAGE_LIMIT:
            messages.error(self.request, TOO_MANY)
            return self.render_to_response(self.get_context_data(form=form))
        cache.set(key, sent + 1, LIMIT_SECONDS)
        # Bots get the same thank you, so they cannot tell they were
        # caught, but their message is not saved.
        if not form.is_spam():
            form.save()
        messages.success(self.request, THANK_YOU)
        return redirect("home")
