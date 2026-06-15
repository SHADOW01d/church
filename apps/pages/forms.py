from django import forms

from .models import ContactMessage


class ContactForm(forms.ModelForm):
    """Public contact form.

    A ModelForm gives us server-side validation and ORM-parameterised
    writes for free (OWASP A03: Injection). All rendered values are
    auto-escaped by the Django template engine (XSS protection).
    """

    # Honeypot field: real users never see/fill it; bots often do.
    website = forms.CharField(required=False, widget=forms.HiddenInput)

    class Meta:
        model = ContactMessage
        fields = ["name", "email", "phone", "subject", "message"]
        widgets = {
            "name": forms.TextInput(attrs={"placeholder": "Jina Lako Kamili", "autocomplete": "name", "aria-label": "Jina kamili"}),
            "email": forms.EmailInput(attrs={"placeholder": "Anwani Yako ya Barua Pepe", "autocomplete": "email", "aria-label": "Barua pepe"}),
            "phone": forms.TextInput(attrs={"placeholder": "Namba ya Simu (si lazima)", "autocomplete": "tel", "aria-label": "Namba ya simu"}),
            "subject": forms.TextInput(attrs={"placeholder": "Mada", "aria-label": "Mada ya ujumbe"}),
            "message": forms.Textarea(attrs={"placeholder": "Ujumbe wako au ombi la maombi...", "rows": 5, "aria-label": "Ujumbe"}),
        }

    def clean_website(self):
        if self.cleaned_data.get("website"):
            raise forms.ValidationError("Spam detected.")
        return ""
