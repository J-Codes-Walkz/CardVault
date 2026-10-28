"""Django admin set-up for accounts."""
from allauth.account.models import EmailAddress
from django.contrib import admin

# CardVault never collects email addresses (see the Privacy page), so
# django-allauth's Email addresses section would always be empty.
admin.site.unregister(EmailAddress)
