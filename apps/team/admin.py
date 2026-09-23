from django.contrib import admin

from .models import Consultant


@admin.register(Consultant)
class ConsultantAdmin(admin.ModelAdmin):
    list_display = ("name", "designation", "department", "is_active", "order")
    list_editable = ("is_active", "order")
    list_filter = ("department", "is_active")
    search_fields = ("name", "designation", "bio")
    prepopulated_fields = {"slug": ("name",)}
