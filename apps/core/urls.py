from django.urls import path

from . import views

app_name = "core"

urlpatterns = [
    path("", views.HomeView.as_view(), name="home"),
    path("about/", views.AboutView.as_view(), name="about"),
    path("testimonials/", views.TestimonialListView.as_view(), name="testimonials"),
    path("faq/", views.FAQView.as_view(), name="faq"),
    path("careers/", views.CareerListView.as_view(), name="careers"),
    path("careers/<slug:slug>/", views.CareerDetailView.as_view(), name="career_detail"),
    path("search/", views.SearchView.as_view(), name="search"),
    path("privacy-policy/", views.StaticPageView.as_view(), {"slug": "privacy-policy"}, name="privacy_policy"),
    path("terms-conditions/", views.StaticPageView.as_view(), {"slug": "terms-conditions"}, name="terms_conditions"),
    path("page/<slug:slug>/", views.StaticPageView.as_view(), name="static_page"),
]
