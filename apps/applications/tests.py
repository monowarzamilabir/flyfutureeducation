from django.core import mail
from django.test import TestCase
from django.urls import reverse

from .models import Application


class ApplicationFormSubmissionTests(TestCase):
    def setUp(self):
        self.url = reverse("applications:apply")
        self.valid_data = {
            "website": "",  # honeypot must stay empty
            "full_name": "Rakib Hasan",
            "email": "rakib@example.com",
            "phone": "01700000000",
            "country": "",
            "desired_program": "masters",
            "preferred_intake": "September 2026",
            "message": "I would like to study computer science abroad.",
        }

    def test_get_returns_200(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_valid_submission_creates_application_and_sends_emails(self):
        response = self.client.post(self.url, self.valid_data, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Application.objects.count(), 1)
        application = Application.objects.first()
        self.assertEqual(application.full_name, "Rakib Hasan")
        self.assertEqual(application.status, "new")
        # One email to admin, one confirmation email to the applicant.
        self.assertEqual(len(mail.outbox), 2)

    def test_honeypot_field_blocks_submission(self):
        data = self.valid_data | {"website": "http://spam.example.com"}
        self.client.post(self.url, data)
        self.assertEqual(Application.objects.count(), 0)

    def test_missing_required_field_does_not_create_application(self):
        data = self.valid_data | {"full_name": ""}
        self.client.post(self.url, data)
        self.assertEqual(Application.objects.count(), 0)
