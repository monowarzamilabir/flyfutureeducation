from ckeditor_uploader.fields import RichTextUploadingField
from django.db import models
from django.urls import reverse

from apps.core.models import SEOModel, SlugFromFieldMixin, TimeStampedModel


class TestPrepCourse(SEOModel, TimeStampedModel, SlugFromFieldMixin):
    """A test-prep / coaching course, e.g. IELTS, TOEFL, PTE, Duolingo."""

    slug_source_field = "title"

    title = models.CharField(max_length=150)
    slug = models.SlugField(max_length=170, unique=True, blank=True)
    image = models.ImageField(upload_to="trainings/", blank=True, null=True)
    short_description = models.CharField(max_length=255, blank=True)
    description = RichTextUploadingField()
    duration = models.CharField(max_length=100, blank=True, help_text="e.g. '6 weeks, 3 classes/week'")
    fee = models.CharField(max_length=100, blank=True, help_text="e.g. 'BDT 8,000'")
    schedule_info = RichTextUploadingField(blank=True)
    is_featured = models.BooleanField(default=False)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["order", "title"]
        verbose_name = "Test Prep Course"

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("trainings:detail", kwargs={"slug": self.slug})
