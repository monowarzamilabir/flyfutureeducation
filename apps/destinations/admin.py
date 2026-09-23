from django.contrib import admin

from .models import Country, University


class UniversityInline(admin.TabularInline):
    model = University
    extra = 1
    fields = ("name", "logo", "ranking", "tuition_range", "website_url", "order")


@admin.register(Country)
class CountryAdmin(admin.ModelAdmin):
    list_display = ("name", "intake_seasons", "is_featured", "order", "updated_at")
    list_editable = ("is_featured", "order")
    list_filter = ("is_featured",)
    search_fields = ("name", "overview", "visa_requirements")
    prepopulated_fields = {"slug": ("name",)}
    inlines = [UniversityInline]
    fieldsets = (
        (None, {"fields": ("name", "slug", "flag_image", "hero_image")}),
        ("Content", {"fields": ("overview", "why_study_here", "visa_requirements", "work_rights")}),
        ("Facts", {"fields": ("cost_of_living", "tuition_range", "intake_seasons")}),
        ("Display", {"fields": ("is_featured", "order")}),
        ("SEO", {"fields": ("meta_title", "meta_description")}),
    )


@admin.register(University)
class UniversityAdmin(admin.ModelAdmin):
    list_display = ("name", "country", "ranking", "tuition_range", "order")
    list_editable = ("order",)
    list_filter = ("country",)
    search_fields = ("name", "programs_offered")
