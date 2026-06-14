from django import forms

from .models import ContactMessage


class ContactForm(forms.ModelForm):
    """Public contact form.

    A ModelForm gives us server-side validation and ORM-parameterised
    writes for free (OWASP A03: Injection). All rendered values are
    auto-escaped by the Django template engine (XSS protection).
    """

    INTEREST_CHOICES = [
        ("Visiting for the First Time", "Visiting for the First Time"),
        ("Joining a Ministry", "Joining a Ministry"),
        ("Prayer Request", "Prayer Request"),
        ("Marriage Counselling", "Marriage Counselling"),
        ("General Enquiry", "General Enquiry"),
    ]

    subject = forms.ChoiceField(
        choices=INTEREST_CHOICES, required=False, label="I am interested in..."
    )

    # Honeypot field: real users never see/fill it; bots often do.
    website = forms.CharField(required=False, widget=forms.HiddenInput)

    class Meta:
        model = ContactMessage
        fields = ["name", "email", "phone", "subject", "message"]
        widgets = {
            "name": forms.TextInput(attrs={"placeholder": "Your name", "autocomplete": "name"}),
            "email": forms.EmailInput(attrs={"placeholder": "you@example.com", "autocomplete": "email"}),
            "phone": forms.TextInput(attrs={"placeholder": "Phone (optional)", "autocomplete": "tel"}),
            "subject": forms.TextInput(attrs={"placeholder": "Subject"}),
            "message": forms.Textarea(attrs={"placeholder": "How can we pray with you?", "rows": 5}),
        }

    def clean_website(self):
        if self.cleaned_data.get("website"):
            raise forms.ValidationError("Spam detected.")
        return ""
