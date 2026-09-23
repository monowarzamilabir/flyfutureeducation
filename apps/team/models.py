from ckeditor_uploader.fields import RichTextUploadingField
from django.db import models
from django.urls import reverse

from apps.core.models import SlugFromFieldMixin, TimeStampedModel


class Consultant(TimeStampedModel, SlugFromFieldMixin):
    slug_source_field = "name"

    DEPARTMENT_CHOICES = [
        ("admissions", "Admissions"),
        ("visa", "Visa Processing"),
        ("counselling", "Counselling"),
        ("test_prep", "Test Prep"),
        ("management", "Management"),
    ]

    name = models.CharField(max_length=120)
    slug = models.SlugField(max_length=140, unique=True, blank=True)
    designation = models.CharField(max_length=150)
    department = models.CharField(max_length=30, choices=DEPARTMENT_CHOICES, default="counselling")
    photo = models.ImageField(upload_to="team/", blank=True, null=True)
    bio = RichTextUploadingField(blank=True)
    email = models.EmailField(blank=True)
    phone = models.CharField(max_length=40, blank=True)
    facebook_url = models.URLField(blank=True)
    linkedin_url = models.URLField(blank=True)
    is_active = models.BooleanField(default=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["order", "name"]

    def __str__(self):
        return f"{self.name} — {self.designation}"

    def get_absolute_url(self):
        return reverse("team:detail", kwargs={"slug": self.slug})
