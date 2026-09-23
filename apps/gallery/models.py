from django.db import models
from django.urls import reverse
from django.utils.text import slugify

from apps.core.models import TimeStampedModel


class PhotoAlbum(TimeStampedModel):
    title = models.CharField(max_length=150)
    slug = models.SlugField(max_length=170, unique=True, blank=True)
    cover_image = models.ImageField(upload_to="gallery/covers/", blank=True, null=True)
    description = models.CharField(max_length=255, blank=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["order", "-created_at"]

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.title)[:160]
            slug = base_slug
            counter = 2
            while PhotoAlbum.objects.filter(slug=slug).exclude(pk=self.pk).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            self.slug = slug
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("gallery:album_detail", kwargs={"slug": self.slug})


class Photo(TimeStampedModel):
    album = models.ForeignKey(PhotoAlbum, on_delete=models.CASCADE, related_name="photos")
    image = models.ImageField(upload_to="gallery/photos/")
    caption = models.CharField(max_length=200, blank=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["order", "-created_at"]

    def __str__(self):
        return self.caption or f"Photo #{self.pk}"


class VideoItem(TimeStampedModel):
    title = models.CharField(max_length=150)
    video_id = models.CharField(
        max_length=50,
        help_text="YouTube video ID (the part after 'v=' or after youtu.be/), e.g. 'dQw4w9WgXcQ'.",
    )
    thumbnail = models.ImageField(upload_to="gallery/video_thumbs/", blank=True, null=True)
    description = models.CharField(max_length=255, blank=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["order", "-created_at"]

    def __str__(self):
        return self.title

    @property
    def embed_url(self):
        return f"https://www.youtube.com/embed/{self.video_id}"

    @property
    def thumbnail_url(self):
        if self.thumbnail:
            return self.thumbnail.url
        return f"https://img.youtube.com/vi/{self.video_id}/hqdefault.jpg"
