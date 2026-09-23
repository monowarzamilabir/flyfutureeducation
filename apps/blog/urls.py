from django.urls import path

from . import views

app_name = "blog"

urlpatterns = [
    path("", views.PostListView.as_view(), name="list"),
    path("category/<slug:slug>/", views.PostListView.as_view(), name="category"),
    path("tag/<slug:slug>/", views.PostListView.as_view(), name="tag"),
    path("<slug:slug>/", views.PostDetailView.as_view(), name="detail"),
]
