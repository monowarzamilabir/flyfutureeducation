from django.contrib import admin

from .models import Service


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ("title", "short_description", "is_featured", "order", "updated_at")
    list_editable = ("is_featured", "order")
    list_filter = ("is_featured",)
    search_fields = ("title", "short_description", "body")
    prepopulated_fields = {"slug": ("title",)}
    fieldsets = (
        (None, {"fields": ("title", "slug", "icon", "image", "short_description", "body")}),
        ("Display", {"fields": ("is_featured", "order")}),
        ("SEO", {"fields": ("meta_title", "meta_description")}),
    )
