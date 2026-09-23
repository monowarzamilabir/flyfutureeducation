from django.contrib import admin

from .models import Scholarship


@admin.register(Scholarship)
class ScholarshipAdmin(admin.ModelAdmin):
    list_display = ("title", "country", "amount_coverage", "deadline", "is_featured", "order")
    list_editable = ("is_featured", "order")
    list_filter = ("is_featured", "country")
    search_fields = ("title", "amount_coverage", "eligibility")
    prepopulated_fields = {"slug": ("title",)}
    date_hierarchy = "deadline"
    fieldsets = (
        (None, {"fields": ("title", "slug", "country", "image", "amount_coverage", "description", "eligibility")}),
        ("Application", {"fields": ("deadline", "apply_link")}),
        ("Display", {"fields": ("is_featured", "order")}),
        ("SEO", {"fields": ("meta_title", "meta_description")}),
    )
