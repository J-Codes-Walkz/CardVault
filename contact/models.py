"""Messages sent through the Contact page."""
from django.db import models


class ContactMessage(models.Model):
    """One enquiry, read and answered by hand from the Django admin."""

    name = models.CharField(max_length=100)
    email = models.EmailField()
    message = models.TextField(max_length=2000)
    handled = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        """The sender and date, for example "Ash (29 Oct 2026)"."""
        return f"{self.name} ({self.created_at:%d %b %Y})"
