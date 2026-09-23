from django.contrib import admin

from .models import (
    FAQ,
    Benefit,
    FAQCategory,
    JobApplication,
    JobPosting,
    ProcessStep,
    SiteSettings,
    SiteStat,
    StaticPage,
    Testimonial,
)


@admin.register(SiteSettings)
class SiteSettingsAdmin(admin.ModelAdmin):
    fieldsets = (
        ("Branding", {"fields": ("site_name", "tagline", "logo", "favicon", "about_short")}),
        ("Contact", {"fields": ("phone_primary", "whatsapp_number", "email", "address", "office_hours", "google_map_embed_url")}),
        ("Social links", {"fields": ("facebook_url", "instagram_url", "linkedin_url", "youtube_url", "messenger_url")}),
        ("Footer", {"fields": ("footer_text",)}),
        ("Default SEO / Open Graph", {"fields": ("default_meta_title", "default_meta_description", "default_og_image")}),
    )

    def has_add_permission(self, request):
        return not SiteSettings.objects.exists()

    def has_delete_permission(self, request, obj=None):
        return False

    def changelist_view(self, request, extra_context=None):
        obj = SiteSettings.load()
        from django.shortcuts import redirect
        from django.urls import reverse

        return redirect(reverse("admin:core_sitesettings_change", args=[obj.pk]))


@admin.register(Testimonial)
class TestimonialAdmin(admin.ModelAdmin):
    list_display = ("name", "role", "country", "rating", "is_featured", "order", "created_at")
    list_editable = ("is_featured", "order")
    list_filter = ("is_featured", "rating", "country")
    search_fields = ("name", "role", "message")
    ordering = ("order", "-created_at")


class FAQInline(admin.TabularInline):
    model = FAQ
    extra = 1
    fields = ("question", "answer", "order", "is_published")


@admin.register(FAQCategory)
class FAQCategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "slug", "order")
    prepopulated_fields = {"slug": ("name",)}
    ordering = ("order", "name")
    inlines = [FAQInline]


@admin.register(FAQ)
class FAQAdmin(admin.ModelAdmin):
    list_display = ("question", "category", "order", "is_published", "created_at")
    list_editable = ("order", "is_published")
    list_filter = ("category", "is_published")
    search_fields = ("question", "answer")


@admin.register(StaticPage)
class StaticPageAdmin(admin.ModelAdmin):
    list_display = ("title", "slug", "updated_at")
    prepopulated_fields = {"slug": ("title",)}
    search_fields = ("title", "body")
    fieldsets = (
        (None, {"fields": ("title", "slug", "body")}),
        ("SEO", {"fields": ("meta_title", "meta_description")}),
    )


@admin.register(ProcessStep)
class ProcessStepAdmin(admin.ModelAdmin):
    list_display = ("step_number", "title", "order")
    list_editable = ("order",)
    ordering = ("order", "step_number")


@admin.register(Benefit)
class BenefitAdmin(admin.ModelAdmin):
    list_display = ("title", "order")
    list_editable = ("order",)
    ordering = ("order",)


@admin.register(SiteStat)
class SiteStatAdmin(admin.ModelAdmin):
    list_display = ("label", "value", "suffix", "order")
    list_editable = ("value", "suffix", "order")
    ordering = ("order",)


class JobApplicationInline(admin.TabularInline):
    model = JobApplication
    extra = 0
    fields = ("full_name", "email", "phone", "resume", "created_at")
    readonly_fields = ("created_at",)
    can_delete = False


@admin.register(JobPosting)
class JobPostingAdmin(admin.ModelAdmin):
    list_display = ("title", "department", "location", "employment_type", "is_active", "application_deadline")
    list_editable = ("is_active",)
    list_filter = ("is_active", "employment_type", "department")
    search_fields = ("title", "department", "description")
    prepopulated_fields = {"slug": ("title",)}
    inlines = [JobApplicationInline]


@admin.register(JobApplication)
class JobApplicationAdmin(admin.ModelAdmin):
    list_display = ("full_name", "job", "email", "phone", "created_at")
    list_filter = ("job",)
    search_fields = ("full_name", "email", "phone")


admin.site.site_header = "Fly Future Education Admin"
admin.site.site_title = "Fly Future Education Admin"
admin.site.index_title = "Site Administration"
