from django.contrib import admin

from .models import Application


@admin.register(Application)
class ApplicationAdmin(admin.ModelAdmin):
    list_display = ("full_name", "email", "phone", "country", "desired_program", "status", "created_at")
    list_editable = ("status",)
    list_filter = ("status", "country", "desired_program", "created_at")
    search_fields = ("full_name", "email", "phone", "message")
    date_hierarchy = "created_at"
    readonly_fields = ("created_at", "updated_at")
    fieldsets = (
        ("Applicant", {"fields": ("full_name", "email", "phone")}),
        ("Study Plan", {"fields": ("country", "desired_program", "preferred_intake", "message", "document")}),
        ("Staff Triage", {"fields": ("status", "staff_notes")}),
        ("Timestamps", {"fields": ("created_at", "updated_at")}),
    )
