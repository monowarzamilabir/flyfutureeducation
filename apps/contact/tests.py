from django.core import mail
from django.test import TestCase
from django.urls import reverse

from .models import ContactMessage


class ContactFormSubmissionTests(TestCase):
    def setUp(self):
        self.url = reverse("contact:contact")
        self.valid_data = {
            "website": "",
            "name": "Nusrat Jahan",
            "email": "nusrat@example.com",
            "phone": "01800000000",
            "subject": "Question about IELTS",
            "message": "Do I need IELTS for the Malaysia intake?",
        }

    def test_get_returns_200(self):
        self.assertEqual(self.client.get(self.url).status_code, 200)

    def test_valid_submission_creates_message_and_sends_email(self):
        self.client.post(self.url, self.valid_data, follow=True)
        self.assertEqual(ContactMessage.objects.count(), 1)
        self.assertEqual(len(mail.outbox), 1)
        self.assertIn("Question about IELTS", mail.outbox[0].subject)

    def test_honeypot_blocks_submission(self):
        data = self.valid_data | {"website": "http://spam.example.com"}
        self.client.post(self.url, data)
        self.assertEqual(ContactMessage.objects.count(), 0)
