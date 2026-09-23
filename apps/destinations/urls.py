from django.urls import path

from . import views

app_name = "destinations"

urlpatterns = [
    path("", views.CountryListView.as_view(), name="list"),
    path("<slug:slug>/", views.CountryDetailView.as_view(), name="detail"),
]
