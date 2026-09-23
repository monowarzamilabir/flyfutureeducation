from django import forms

from .models import JobApplication


class HoneypotMixin(forms.Form):
    """Adds an invisible honeypot field for basic spam protection on public forms."""

    website = forms.CharField(
        required=False,
        widget=forms.TextInput(
            attrs={"class": "hp-field", "tabindex": "-1", "autocomplete": "off", "aria-hidden": "true"}
        ),
        label="",
    )

    def clean_website(self):
        value = self.cleaned_data.get("website")
        if value:
            raise forms.ValidationError("Spam detected.")
        return value


class StyledFormMixin:
    """Applies the shared Tailwind 'form-input' class to every visible field's widget."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for name, field in self.fields.items():
            if name == "website":  # honeypot keeps its own hidden styling
                continue
            existing = field.widget.attrs.get("class", "")
            field.widget.attrs["class"] = (existing + " form-input").strip()


class JobApplicationForm(StyledFormMixin, HoneypotMixin, forms.ModelForm):
    class Meta:
        model = JobApplication
        fields = ["full_name", "email", "phone", "cover_note", "resume"]
        widgets = {
            "full_name": forms.TextInput(attrs={"placeholder": "Your full name", "required": True}),
            "email": forms.EmailInput(attrs={"placeholder": "you@example.com", "required": True}),
            "phone": forms.TextInput(attrs={"placeholder": "01XXXXXXXXX", "required": True}),
            "cover_note": forms.Textarea(attrs={"rows": 4, "placeholder": "Tell us why you're a great fit (optional)"}),
        }
