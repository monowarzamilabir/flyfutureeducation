from ckeditor_uploader.fields import RichTextUploadingField
from django.core.exceptions import ValidationError
from django.db import models
from django.utils.text import slugify


class TimeStampedModel(models.Model):
    """Abstract base adding created/updated timestamps."""

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class SEOModel(models.Model):
    """Abstract base adding per-page SEO fields."""

    meta_title = models.CharField(
        max_length=70,
        blank=True,
        help_text="Overrides the <title> tag. Falls back to the page title if left blank. Aim for under 60 characters.",
    )
    meta_description = models.CharField(
        max_length=160,
        blank=True,
        help_text="Search-result snippet. Aim for 120-160 characters.",
    )

    class Meta:
        abstract = True


class SlugFromFieldMixin(models.Model):
    """Abstract base that auto-generates a unique slug from `slug_source_field` on save."""

    slug_source_field = "title"

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(getattr(self, self.slug_source_field))[:190]
            slug = base_slug
            counter = 2
            model = self.__class__
            while model.objects.filter(slug=slug).exclude(pk=self.pk).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            self.slug = slug
        super().save(*args, **kwargs)


class SiteSettings(models.Model):
    """Singleton model holding global, admin-editable site content."""

    site_name = models.CharField(max_length=120, default="Fly Future Education")
    tagline = models.CharField(max_length=200, default="Empowering Dreams Through Global Education")
    logo = models.ImageField(upload_to="site/", blank=True, null=True)
    favicon = models.ImageField(upload_to="site/", blank=True, null=True)

    about_short = models.TextField(
        blank=True,
        help_text="A short 2-3 sentence summary used in the footer and social previews.",
    )

    phone_primary = models.CharField(max_length=40, default="+880 1805-030201")
    whatsapp_number = models.CharField(
        max_length=40,
        default="8801805030201",
        help_text="Digits only with country code, no + or spaces (used to build wa.me links).",
    )
    email = models.EmailField(default="flufutureeducation@gmail.com")
    address = models.TextField(default="25/5/A Pragati Sharani, Shahjadpur, Gulshan, Dhaka -1212.")
    office_hours = models.CharField(
        max_length=200,
        default="Sat - Thu: 10:00 AM - 7:00 PM | Friday: Closed",
    )
    google_map_embed_url = models.URLField(
        blank=True,
        help_text="Paste the 'src' URL from a Google Maps embed iframe for the office address.",
    )

    facebook_url = models.URLField(blank=True, default="https://www.facebook.com/flyfutureeducationbd/")
    instagram_url = models.URLField(blank=True)
    linkedin_url = models.URLField(blank=True)
    youtube_url = models.URLField(blank=True)
    messenger_url = models.URLField(
        blank=True,
        help_text="Link used by the floating Messenger chat bubble, e.g. https://m.me/flyfutureeducationbd",
    )

    footer_text = models.CharField(
        max_length=200,
        default="Fly Future Education — Empowering Dreams Through Global Education.",
    )

    default_meta_title = models.CharField(max_length=70, default="Fly Future Education | Study Abroad Consultants in Dhaka")
    default_meta_description = models.CharField(
        max_length=160,
        default="Fly Future Education helps Bangladeshi students study abroad with expert visa processing, university admissions, scholarship and IELTS/PTE guidance.",
    )
    default_og_image = models.ImageField(upload_to="site/", blank=True, null=True)

    class Meta:
        verbose_name = "Site Settings"
        verbose_name_plural = "Site Settings"

    def __str__(self):
        return "Site Settings"

    def save(self, *args, **kwargs):
        self.pk = 1
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        pass  # singleton: never actually delete

    @classmethod
    def load(cls):
        obj, _ = cls.objects.get_or_create(pk=1)
        return obj


class Testimonial(TimeStampedModel):
    RATING_CHOICES = [(i, str(i)) for i in range(1, 6)]

    name = models.CharField(max_length=120)
    role = models.CharField(
        max_length=150,
        blank=True,
        help_text="e.g. 'Now studying at University of Toronto, Canada'",
    )
    photo = models.ImageField(upload_to="testimonials/", blank=True, null=True)
    country = models.CharField(max_length=80, blank=True)
    message = models.TextField()
    rating = models.PositiveSmallIntegerField(choices=RATING_CHOICES, default=5)
    is_featured = models.BooleanField(default=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["order", "-created_at"]

    def __str__(self):
        return f"{self.name} ({self.rating}★)"


class FAQCategory(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=110, unique=True, blank=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        verbose_name = "FAQ Category"
        verbose_name_plural = "FAQ Categories"
        ordering = ["order", "name"]

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class FAQ(TimeStampedModel):
    category = models.ForeignKey(FAQCategory, on_delete=models.CASCADE, related_name="faqs")
    question = models.CharField(max_length=255)
    answer = RichTextUploadingField()
    order = models.PositiveIntegerField(default=0)
    is_published = models.BooleanField(default=True)

    class Meta:
        verbose_name = "FAQ"
        verbose_name_plural = "FAQs"
        ordering = ["category__order", "order"]

    def __str__(self):
        return self.question


class StaticPage(SEOModel, TimeStampedModel, SlugFromFieldMixin):
    slug_source_field = "title"

    title = models.CharField(max_length=150)
    slug = models.SlugField(max_length=160, unique=True, blank=True)
    body = RichTextUploadingField()

    class Meta:
        ordering = ["title"]

    def __str__(self):
        return self.title


class ProcessStep(models.Model):
    """A step in the homepage 'How it works' 4-step process section."""

    step_number = models.PositiveSmallIntegerField()
    title = models.CharField(max_length=100)
    description = models.CharField(max_length=255)
    icon = models.CharField(
        max_length=50,
        blank=True,
        help_text="Emoji or short icon label, e.g. 'search', 'file', 'visa', 'plane'.",
    )
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["order", "step_number"]

    def __str__(self):
        return f"Step {self.step_number}: {self.title}"


class Benefit(models.Model):
    """A 'Why choose us' benefit tile shown on the homepage."""

    title = models.CharField(max_length=100)
    description = models.CharField(max_length=255)
    icon = models.CharField(max_length=50, blank=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["order"]

    def __str__(self):
        return self.title


class SiteStat(models.Model):
    """A homepage stats-counter tile, e.g. '3000+ Students Placed'."""

    label = models.CharField(max_length=100)
    value = models.PositiveIntegerField()
    suffix = models.CharField(max_length=10, blank=True, default="+")
    icon = models.CharField(max_length=50, blank=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["order"]

    def __str__(self):
        return f"{self.label}: {self.value}{self.suffix}"


class JobPosting(SEOModel, TimeStampedModel, SlugFromFieldMixin):
    """Careers page job listing."""

    slug_source_field = "title"

    EMPLOYMENT_TYPES = [
        ("full_time", "Full-time"),
        ("part_time", "Part-time"),
        ("internship", "Internship"),
        ("contract", "Contract"),
    ]

    title = models.CharField(max_length=150)
    slug = models.SlugField(max_length=170, unique=True, blank=True)
    department = models.CharField(max_length=100, blank=True)
    location = models.CharField(max_length=100, default="Dhaka, Bangladesh")
    employment_type = models.CharField(max_length=20, choices=EMPLOYMENT_TYPES, default="full_time")
    description = RichTextUploadingField()
    is_active = models.BooleanField(default=True)
    application_deadline = models.DateField(blank=True, null=True)

    class Meta:
        ordering = ["-is_active", "-created_at"]

    def __str__(self):
        return self.title


class JobApplication(TimeStampedModel):
    job = models.ForeignKey(JobPosting, on_delete=models.CASCADE, related_name="applications")
    full_name = models.CharField(max_length=150)
    email = models.EmailField()
    phone = models.CharField(max_length=30)
    cover_note = models.TextField(blank=True)
    resume = models.FileField(upload_to="career_applications/%Y/%m/")

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.full_name} -> {self.job}"

    def clean(self):
        if self.resume:
            ext = self.resume.name.lower().rsplit(".", 1)[-1]
            if ext not in {"pdf", "doc", "docx"}:
                raise ValidationError({"resume": "Resume must be a PDF or Word document."})
