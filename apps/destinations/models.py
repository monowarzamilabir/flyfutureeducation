from ckeditor_uploader.fields import RichTextUploadingField
from django.db import models
from django.urls import reverse

from apps.core.models import SEOModel, SlugFromFieldMixin, TimeStampedModel


class Country(SEOModel, TimeStampedModel, SlugFromFieldMixin):
    """A study destination country."""

    slug_source_field = "name"

    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=110, unique=True, blank=True)
    flag_image = models.ImageField(upload_to="destinations/flags/", blank=True, null=True)
    hero_image = models.ImageField(upload_to="destinations/hero/", blank=True, null=True)

    overview = RichTextUploadingField(blank=True)
    why_study_here = RichTextUploadingField(blank=True)
    visa_requirements = RichTextUploadingField(blank=True)
    work_rights = RichTextUploadingField(
        blank=True,
        help_text="Post-study work (PSW) rights and work-while-studying information.",
    )

    cost_of_living = models.CharField(max_length=150, blank=True, help_text="e.g. 'BDT 60,000 - 90,000 / month'")
    tuition_range = models.CharField(max_length=150, blank=True, help_text="e.g. 'BDT 6,00,000 - 12,00,000 / year'")
    intake_seasons = models.CharField(max_length=150, blank=True, help_text="e.g. 'February, September'")

    is_featured = models.BooleanField(default=False, help_text="Featured destinations appear on the homepage.")
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["order", "name"]
        verbose_name_plural = "Countries"

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("destinations:detail", kwargs={"slug": self.slug})


class University(TimeStampedModel):
    country = models.ForeignKey(Country, on_delete=models.CASCADE, related_name="universities")
    name = models.CharField(max_length=200)
    logo = models.ImageField(upload_to="destinations/universities/", blank=True, null=True)
    ranking = models.CharField(max_length=100, blank=True, help_text="e.g. 'QS World Rank #120'")
    programs_offered = models.TextField(blank=True, help_text="Comma-separated or short free text list.")
    tuition_range = models.CharField(max_length=150, blank=True)
    website_url = models.URLField(blank=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["order", "name"]
        verbose_name_plural = "Universities"

    def __str__(self):
        return f"{self.name} ({self.country.name})"
