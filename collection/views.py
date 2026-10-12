"""Views for a user's own cards."""
from django.contrib.auth.decorators import login_required
from django.shortcuts import render


@login_required
def my_cards(request):
    """List the logged-in user's own entries, newest first."""
    entries = request.user.collection_entries.select_related("card")
    return render(request, "collection/my_cards.html", {"entries": entries})
