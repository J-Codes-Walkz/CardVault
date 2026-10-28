"""Django admin registration for contact messages."""
from django.contrib import admin

from .models import ContactMessage


@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ("name", "email", "created_at", "handled")
    list_filter = ("handled",)
    list_editable = ("handled",)
    search_fields = ("name", "email", "message")
    readonly_fields = ("name", "email", "message", "created_at")

    def has_add_permission(self, request):
        """Messages only ever come from visitors, never from the admin."""
        return False
