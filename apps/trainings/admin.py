from django.contrib import admin

from .models import TestPrepCourse


@admin.register(TestPrepCourse)
class TestPrepCourseAdmin(admin.ModelAdmin):
    list_display = ("title", "duration", "fee", "is_featured", "order")
    list_editable = ("is_featured", "order")
    list_filter = ("is_featured",)
    search_fields = ("title", "description")
    prepopulated_fields = {"slug": ("title",)}
    fieldsets = (
        (None, {"fields": ("title", "slug", "image", "short_description", "description")}),
        ("Schedule & Fees", {"fields": ("duration", "fee", "schedule_info")}),
        ("Display", {"fields": ("is_featured", "order")}),
        ("SEO", {"fields": ("meta_title", "meta_description")}),
    )
