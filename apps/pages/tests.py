from django.test import TestCase
from django.urls import reverse

from .models import ContactMessage


class HomePageTests(TestCase):
    def test_home_page_renders(self):
        response = self.client.get(reverse("pages:home"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Gilgal Dominion Center")
        self.assertTemplateUsed(response, "pages/home.html")

    def test_security_headers_present(self):
        response = self.client.get(reverse("pages:home"))
        self.assertEqual(response.headers.get("X-Frame-Options"), "DENY")
        self.assertEqual(response.headers.get("X-Content-Type-Options"), "nosniff")


class ContactFormTests(TestCase):
    def test_valid_submission_is_saved(self):
        response = self.client.post(
            reverse("pages:home"),
            {
                "name": "Mary Mwita",
                "email": "mary@example.com",
                "phone": "",
                "subject": "Prayer Request",
                "message": "Please pray for my family.",
                "website": "",
            },
        )
        self.assertEqual(response.status_code, 302)
        self.assertEqual(ContactMessage.objects.count(), 1)
        msg = ContactMessage.objects.get()
        self.assertEqual(msg.name, "Mary Mwita")

    def test_invalid_submission_is_rejected(self):
        response = self.client.post(
            reverse("pages:home"),
            {"name": "", "email": "not-an-email", "message": "", "website": ""},
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(ContactMessage.objects.count(), 0)

    def test_honeypot_blocks_spam(self):
        response = self.client.post(
            reverse("pages:home"),
            {
                "name": "Bot",
                "email": "bot@example.com",
                "message": "spammy",
                "website": "http://spam.example",
            },
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(ContactMessage.objects.count(), 0)
