from django.contrib import messages
from django.urls import reverse
from django.views.generic.edit import FormView

from .forms import ContactForm


class HomeView(FormView):
    """Single-page site homepage.

    Renders all sections and processes the contact form. CSRF protection
    is enforced by Django's middleware + the ``{% csrf_token %}`` tag in
    the template.
    """

    template_name = "pages/home.html"
    form_class = ContactForm

    def get_success_url(self):
        return f"{reverse('pages:home')}#contact"

    def form_valid(self, form):
        form.save()
        messages.success(
            self.request,
            "Message sent! God bless you — we'll be in touch soon.",
        )
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(
            self.request,
            "Please correct the errors below and try again.",
        )
        return super().form_invalid(form)
