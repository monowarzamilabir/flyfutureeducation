from django.urls import path

from . import views

app_name = "scholarships"

urlpatterns = [
    path("", views.ScholarshipListView.as_view(), name="list"),
    path("<slug:slug>/", views.ScholarshipDetailView.as_view(), name="detail"),
]
