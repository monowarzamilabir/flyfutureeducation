from django.urls import path

from . import views

app_name = "gallery"

urlpatterns = [
    path("photos/", views.AlbumListView.as_view(), name="albums"),
    path("photos/<slug:slug>/", views.AlbumDetailView.as_view(), name="album_detail"),
    path("videos/", views.VideoListView.as_view(), name="videos"),
]
