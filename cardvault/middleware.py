"""Security headers added to every page CardVault serves."""

# Content Security Policy: the browser may only load scripts, styles
# and fonts from this site, card pictures from this site or the
# Pokémon TCG image host, and forms may only post back to this site.
# If an attacker ever got HTML into a page, the browser would refuse
# to run it as a script.
CSP_DIRECTIVES = [
    "default-src 'self'",
    "img-src 'self' https://images.pokemontcg.io",
    "script-src 'self'",
    "style-src 'self'",
    "font-src 'self'",
    "connect-src 'self'",
    "form-action 'self'",
    "frame-ancestors 'none'",
    "base-uri 'self'",
    "object-src 'none'",
]
CONTENT_SECURITY_POLICY = "; ".join(CSP_DIRECTIVES)

# Turn off browser features the site never uses.
PERMISSIONS_POLICY = "camera=(), microphone=(), geolocation=(), payment=()"


class SecurityHeadersMiddleware:
    """Add the Content Security Policy and Permissions Policy headers."""

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        csp = "Content-Security-Policy"
        response.headers.setdefault(csp, CONTENT_SECURITY_POLICY)
        response.headers.setdefault("Permissions-Policy", PERMISSIONS_POLICY)
        return response
