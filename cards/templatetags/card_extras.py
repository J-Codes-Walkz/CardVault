"""Template helpers for showing cards and ratings."""
from django import template

register = template.Library()


@register.filter
def stars(rating):
    """Turn a rating such as 4 into filled and empty stars: ★★★★☆."""
    filled = round(rating or 0)
    return "★" * filled + "☆" * (5 - filled)
