from django.views.generic import DetailView, ListView

from .models import PhotoAlbum, VideoItem


class AlbumListView(ListView):
    model = PhotoAlbum
    template_name = "gallery/album_list.html"
    context_object_name = "albums"
    paginate_by = 12

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["meta_title"] = "Photo Gallery | Fly Future Education"
        ctx["meta_description"] = "Browse photos from Fly Future Education events, seminars, and student send-offs."
        return ctx


class AlbumDetailView(DetailView):
    model = PhotoAlbum
    template_name = "gallery/album_detail.html"
    context_object_name = "album"

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        album = ctx["album"]
        ctx["meta_title"] = f"{album.title} | Photo Gallery | Fly Future Education"
        ctx["meta_description"] = album.description
        ctx["photos"] = album.photos.all()
        return ctx


class VideoListView(ListView):
    model = VideoItem
    template_name = "gallery/video_list.html"
    context_object_name = "videos"
    paginate_by = 12

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["meta_title"] = "Video Gallery | Fly Future Education"
        ctx["meta_description"] = "Watch videos from Fly Future Education: student stories, seminars, and destination guides."
        return ctx
