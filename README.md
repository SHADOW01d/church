# Gilgal Dominion Center

A Django website for **Gilgal Dominion Center** ("Mahali Ambapo Mtu Anafaa"),
built from the original `church3swahili.html` single-page design (Swahili). The
static page has been turned into a proper, scalable, security-hardened Django
project. The site's local photos are bundled under `static/img/`.

## Highlights

- **Split settings** (`config/settings/{base,dev,prod}.py`) so dev and prod
  differ safely.
- **Environment-based configuration** via [`django-environ`](https://django-environ.readthedocs.io/)
  — no secrets in source control.
- **Apps live under `apps/`** (`apps.pages`) so new sections/features can be
  added as independent apps.
- **Static assets** (`static/css/main.css`, `static/js/main.js`, `static/img/`)
  served by [WhiteNoise](https://whitenoise.readthedocs.io/) with hashed,
  compressed files.
- **Real backend feature**: the contact form is a Django `ModelForm` with
  server-side validation, CSRF protection, a honeypot anti-spam field, and an
  admin to review submissions.
- **OWASP Top Ten** hardening baked in (see below).

## Project layout

```
.
├── config/                 # Project package
│   ├── settings/           # base.py, dev.py, prod.py
│   ├── middleware.py       # Security headers (CSP, Permissions-Policy)
│   ├── urls.py
│   ├── wsgi.py / asgi.py
├── apps/
│   └── pages/              # Homepage + contact form
│       ├── models.py       # ContactMessage
│       ├── forms.py        # ContactForm (+ honeypot)
│       ├── views.py        # HomeView (FormView)
│       ├── urls.py
│       ├── admin.py
│       └── tests.py
├── templates/
│   ├── base.html
│   └── pages/home.html
├── static/
│   ├── css/main.css
│   └── js/main.js
├── manage.py
├── requirements.txt
└── .env.example
```

## Quick start (development)

```bash
python -m venv .venv
source .venv/bin/activate            # Windows: .venv\Scripts\activate
pip install -r requirements.txt

cp .env.example .env                 # adjust as needed

python manage.py migrate
python manage.py runserver
```

Visit http://127.0.0.1:8000/. The default settings module is
`config.settings.dev` (set in `manage.py`).

Create an admin user to review contact messages:

```bash
python manage.py createsuperuser
# then visit /admin/
```

## Running tests

```bash
python manage.py test
```

## Production

Set environment variables (see `.env.example`) and use the prod settings:

```bash
export DJANGO_SETTINGS_MODULE=config.settings.prod
export DJANGO_SECRET_KEY="$(python -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())')"
export DJANGO_ALLOWED_HOSTS="your-domain.org"
export DJANGO_CSRF_TRUSTED_ORIGINS="https://your-domain.org"

python manage.py migrate
python manage.py collectstatic --noinput
gunicorn config.wsgi:application --bind 0.0.0.0:8000
```

Run the deployment checklist:

```bash
python manage.py check --deploy
```

## OWASP Top Ten — what's addressed

| Risk | Mitigation |
| --- | --- |
| A01 Broken Access Control | Admin behind auth; contact-message admin is read-only. |
| A02 Cryptographic Failures | HSTS, `SECURE_SSL_REDIRECT`, secure + HttpOnly cookies in prod. |
| A03 Injection | ORM/ModelForm (parameterised queries); templates auto-escape (XSS). |
| A04 Insecure Design | Split settings, env-driven config, honeypot on the public form. |
| A05 Security Misconfiguration | `DEBUG=False` in prod, `ALLOWED_HOSTS`, CSP + nosniff + `X-Frame-Options: DENY` + Permissions-Policy. |
| A06 Vulnerable Components | Pinned dependencies in `requirements.txt`. |
| A07 Auth Failures | Django auth + password validators. |
| A08 Integrity Failures | Hashed/manifest static files via WhiteNoise. |
| A09 Logging Failures | Console logging configured in prod. |
| A10 SSRF | No server-side fetching of user-supplied URLs. |

### Known follow-up

The ported markup keeps the original inline `onclick` handlers and inline
`style` attributes, so the Content-Security-Policy currently allows
`'unsafe-inline'` for scripts/styles. Moving those handlers into
`static/js/main.js` would let us drop `'unsafe-inline'` from `script-src`.

## Scaling later

- Swap SQLite for Postgres by setting `DATABASE_URL`.
- Add new pages/features as new apps under `apps/`.
- Static files are CDN-ready (WhiteNoise manifest storage).
- Settings are environment-driven, so the same image runs anywhere.
