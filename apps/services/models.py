from ckeditor_uploader.fields import RichTextUploadingField
from django.db import models
from django.urls import reverse

from apps.core.models import SEOModel, SlugFromFieldMixin, TimeStampedModel


class Service(SEOModel, TimeStampedModel, SlugFromFieldMixin):
    """A service Fly Future Education offers, e.g. Student Visa Support."""

    slug_source_field = "title"

    title = models.CharField(max_length=150)
    slug = models.SlugField(max_length=170, unique=True, blank=True)
    icon = models.CharField(
        max_length=50,
        blank=True,
        help_text="Short icon label used by the card icon, e.g. 'visa', 'passport', 'bank', 'plane'.",
    )
    image = models.ImageField(upload_to="services/", blank=True, null=True)
    short_description = models.CharField(max_length=255)
    body = RichTextUploadingField()
    is_featured = models.BooleanField(default=False, help_text="Featured services appear on the homepage.")
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["order", "title"]

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("services:detail", kwargs={"slug": self.slug})
