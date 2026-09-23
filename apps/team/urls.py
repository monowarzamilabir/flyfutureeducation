from django.urls import path

from . import views

app_name = "team"

urlpatterns = [
    path("", views.ConsultantListView.as_view(), name="list"),
    path("<slug:slug>/", views.ConsultantDetailView.as_view(), name="detail"),
]
