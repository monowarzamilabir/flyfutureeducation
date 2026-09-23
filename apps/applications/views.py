from django.conf import settings
from django.contrib import messages
from django.core.mail import send_mail
from django.shortcuts import redirect, render
from django.views import View

from .forms import ApplicationForm


class ApplyView(View):
    template_name = "applications/apply.html"

    def get(self, request):
        form = ApplicationForm()
        return render(request, self.template_name, self._context(form))

    def post(self, request):
        form = ApplicationForm(request.POST, request.FILES)
        if form.is_valid():
            application = form.save()
            self._notify_admin(application)
            self._confirm_applicant(application)
            messages.success(
                request,
                "Thank you! Your application has been received. A counsellor will contact you within 24 hours.",
            )
            return redirect("applications:apply")
        return render(request, self.template_name, self._context(form))

    def _context(self, form):
        return {
            "form": form,
            "meta_title": "Apply Now | Fly Future Education",
            "meta_description": "Start your study-abroad journey with Fly Future Education. Submit your details and get a free consultation.",
        }

    def _notify_admin(self, application):
        send_mail(
            subject=f"New application: {application.full_name}",
            message=(
                f"Name: {application.full_name}\nEmail: {application.email}\nPhone: {application.phone}\n"
                f"Country: {application.country}\nProgram: {application.get_desired_program_display() if application.desired_program else '-'}\n"
                f"Preferred intake: {application.preferred_intake}\n\nMessage:\n{application.message}"
            ),
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[settings.ADMIN_NOTIFICATION_EMAIL],
            fail_silently=True,
        )

    def _confirm_applicant(self, application):
        send_mail(
            subject="We've received your application — Fly Future Education",
            message=(
                f"Hi {application.full_name},\n\n"
                "Thank you for applying with Fly Future Education. One of our study-abroad consultants "
                "will reach out to you within 24 hours to discuss your options.\n\n"
                "In the meantime, feel free to call or WhatsApp us at 880 1805-030201.\n\n"
                "Warm regards,\nFly Future Education Team"
            ),
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[application.email],
            fail_silently=True,
        )
