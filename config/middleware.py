"""Project-wide HTTP security headers.

Adds a Content-Security-Policy and related headers on top of Django's
built-in protections (X-Frame-Options, nosniff, HSTS). This addresses
OWASP A05 (Security Misconfiguration) and helps mitigate A03 (XSS).

Note: the ported markup uses inline ``onclick`` handlers and inline
``style`` attributes, so ``'unsafe-inline'`` is currently required for
script/style. A future hardening step is to move those handlers into
the external JS file and drop ``'unsafe-inline'`` from ``script-src``.
"""

CSP_POLICY = "; ".join(
    [
        "default-src 'self'",
        "img-src 'self' data: https://images.unsplash.com",
        "style-src 'self' 'unsafe-inline' https://fonts.googleapis.com",
        "font-src 'self' https://fonts.gstatic.com",
        "script-src 'self' 'unsafe-inline'",
        "connect-src 'self'",
        "frame-ancestors 'none'",
        "base-uri 'self'",
        "form-action 'self'",
        "object-src 'none'",
    ]
)

PERMISSIONS_POLICY = "geolocation=(), microphone=(), camera=(), payment=()"


class SecurityHeadersMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        response.setdefault("Content-Security-Policy", CSP_POLICY)
        response.setdefault("Permissions-Policy", PERMISSIONS_POLICY)
        response.setdefault("Cross-Origin-Opener-Policy", "same-origin")
        return response
