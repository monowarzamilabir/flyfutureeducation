from django.db import models

from apps.core.models import TimeStampedModel
from apps.destinations.models import Country


class Application(TimeStampedModel):
    """A submission from the 'Apply Now' multi-field form."""

    STATUS_CHOICES = [
        ("new", "New"),
        ("contacted", "Contacted"),
        ("in_progress", "In Progress"),
        ("converted", "Converted"),
        ("closed", "Closed"),
    ]

    PROGRAM_LEVEL_CHOICES = [
        ("diploma", "Diploma"),
        ("bachelors", "Bachelor's"),
        ("masters", "Master's"),
        ("phd", "PhD"),
        ("language_course", "Language Course"),
    ]

    full_name = models.CharField(max_length=150)
    email = models.EmailField()
    phone = models.CharField(max_length=30)
    country = models.ForeignKey(
        Country, on_delete=models.SET_NULL, null=True, blank=True, related_name="applications"
    )
    desired_program = models.CharField(max_length=150, choices=PROGRAM_LEVEL_CHOICES, blank=True)
    preferred_intake = models.CharField(max_length=100, blank=True, help_text="e.g. 'September 2026'")
    message = models.TextField(blank=True)
    document = models.FileField(
        upload_to="applications/%Y/%m/",
        blank=True,
        null=True,
        help_text="Resume, transcript, or passport copy (PDF/DOC/DOCX/JPG/PNG).",
    )

    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="new")
    staff_notes = models.TextField(blank=True, help_text="Internal notes, not visible to the applicant.")

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.full_name} ({self.get_status_display()})"
