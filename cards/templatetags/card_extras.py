"""Template helpers for showing Poké Ball ratings."""
from django import template
from django.template.loader import render_to_string
from django.utils.html import format_html
from django.utils.safestring import mark_safe

register = template.Library()

# One ball, drawn as inline SVG (templates/includes/ball.svg.html) so
# its colours follow the light or dark theme. Full and empty balls
# differ in shape as well as colour: an empty ball is only an outline.
BALL_TEMPLATE = "includes/ball.svg.html"
BALLS_WRAPPER = '<span class="balls" aria-hidden="true">{}</span>'


def ball(state):
    """The SVG for one ball: "ball-full", "ball-empty" or "ball-pick"."""
    return render_to_string(BALL_TEMPLATE, {"state": state}).strip()


@register.simple_tag
def balls(rating):
    """Five Poké Balls with `rating` of them full, e.g. 4 -> 4 full."""
    full = round(rating or 0)
    states = ["ball-full"] * full + ["ball-empty"] * (5 - full)
    icons = mark_safe("".join(ball(state) for state in states))
    return format_html(BALLS_WRAPPER, icons)


@register.simple_tag
def ball_icon():
    """One Poké Ball for the rating picker; CSS fills it when chosen."""
    return mark_safe(ball("ball-pick"))
