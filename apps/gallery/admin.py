from django.contrib import admin

from .models import PhotoAlbum, Photo, VideoItem


class PhotoInline(admin.TabularInline):
    model = Photo
    extra = 3
    fields = ("image", "caption", "order")


@admin.register(PhotoAlbum)
class PhotoAlbumAdmin(admin.ModelAdmin):
    list_display = ("title", "order", "created_at")
    list_editable = ("order",)
    search_fields = ("title", "description")
    prepopulated_fields = {"slug": ("title",)}
    inlines = [PhotoInline]


@admin.register(VideoItem)
class VideoItemAdmin(admin.ModelAdmin):
    list_display = ("title", "video_id", "order", "created_at")
    list_editable = ("order",)
    search_fields = ("title", "description")
