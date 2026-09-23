from django.conf import settings
from django.contrib import messages
from django.core.mail import send_mail
from django.shortcuts import redirect, render
from django.views import View

from .forms import ContactForm


class ContactView(View):
    template_name = "contact/contact.html"

    def get(self, request):
        form = ContactForm()
        return render(request, self.template_name, self._context(form))

    def post(self, request):
        form = ContactForm(request.POST)
        if form.is_valid():
            contact_message = form.save()
            send_mail(
                subject=f"New contact message: {contact_message.subject or 'No subject'}",
                message=(
                    f"From: {contact_message.name} <{contact_message.email}>\n"
                    f"Phone: {contact_message.phone}\n\n{contact_message.message}"
                ),
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[settings.ADMIN_NOTIFICATION_EMAIL],
                fail_silently=True,
            )
            messages.success(request, "Thanks for reaching out! We'll get back to you shortly.")
            return redirect("contact:contact")
        return render(request, self.template_name, self._context(form))

    def _context(self, form):
        return {
            "form": form,
            "meta_title": "Contact Us | Fly Future Education",
            "meta_description": "Get in touch with Fly Future Education for a free study-abroad consultation. Visit our Dhaka office or call/WhatsApp us.",
        }
