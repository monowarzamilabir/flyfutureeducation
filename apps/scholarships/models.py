from ckeditor_uploader.fields import RichTextUploadingField
from django.db import models
from django.urls import reverse

from apps.core.models import SEOModel, SlugFromFieldMixin, TimeStampedModel
from apps.destinations.models import Country


class Scholarship(SEOModel, TimeStampedModel, SlugFromFieldMixin):
    slug_source_field = "title"

    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=220, unique=True, blank=True)
    country = models.ForeignKey(
        Country, on_delete=models.SET_NULL, null=True, blank=True, related_name="scholarships"
    )
    image = models.ImageField(upload_to="scholarships/", blank=True, null=True)
    amount_coverage = models.CharField(max_length=150, help_text="e.g. 'Up to 50% tuition waiver'")
    description = RichTextUploadingField(blank=True)
    eligibility = RichTextUploadingField()
    deadline = models.DateField(blank=True, null=True)
    apply_link = models.URLField(blank=True)
    is_featured = models.BooleanField(default=False)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["order", "deadline"]

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("scholarships:detail", kwargs={"slug": self.slug})
