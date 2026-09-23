from django import forms

from apps.core.forms import HoneypotMixin, StyledFormMixin

from .models import Application


class ApplicationForm(StyledFormMixin, HoneypotMixin, forms.ModelForm):
    class Meta:
        model = Application
        fields = [
            "full_name",
            "email",
            "phone",
            "country",
            "desired_program",
            "preferred_intake",
            "message",
            "document",
        ]
        widgets = {
            "full_name": forms.TextInput(attrs={"placeholder": "Your full name", "required": True}),
            "email": forms.EmailInput(attrs={"placeholder": "you@example.com", "required": True}),
            "phone": forms.TextInput(attrs={"placeholder": "01XXXXXXXXX", "required": True}),
            "preferred_intake": forms.TextInput(attrs={"placeholder": "e.g. September 2026"}),
            "message": forms.Textarea(attrs={"rows": 4, "placeholder": "Tell us about your study goals (optional)"}),
        }
