import re

from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.contrib.sitemaps.views import sitemap
from django.urls import include, path, re_path
from django.views.generic import RedirectView, TemplateView
from django.views.static import serve as serve_static

from .sitemaps import (
    BlogPostSitemap,
    ConsultantSitemap,
    CountrySitemap,
    ScholarshipSitemap,
    ServiceSitemap,
    StaticViewSitemap,
    TestPrepCourseSitemap,
)

sitemaps = {
    "static": StaticViewSitemap,
    "services": ServiceSitemap,
    "destinations": CountrySitemap,
    "scholarships": ScholarshipSitemap,
    "trainings": TestPrepCourseSitemap,
    "team": ConsultantSitemap,
    "blog": BlogPostSitemap,
}

urlpatterns = [
    path("admin/", admin.site.urls),
    path("ckeditor/", include("ckeditor_uploader.urls")),
    path("accounts/login/", auth_views.LoginView.as_view(template_name="registration/login.html"), name="login"),
    path("accounts/logout/", auth_views.LogoutView.as_view(), name="logout"),
    path("sitemap.xml", sitemap, {"sitemaps": sitemaps}, name="django.contrib.sitemaps.views.sitemap"),
    path("robots.txt", TemplateView.as_view(template_name="robots.txt", content_type="text/plain")),
    path("favicon.ico", RedirectView.as_view(url=settings.STATIC_URL + "img/brand/favicon-32.png", permanent=True)),
    path("services/", include("apps.services.urls")),
    path("destinations/", include("apps.destinations.urls")),
    path("scholarships/", include("apps.scholarships.urls")),
    path("test-prep/", include("apps.trainings.urls")),
    path("team/", include("apps.team.urls")),
    path("apply/", include("apps.applications.urls")),
    path("contact/", include("apps.contact.urls")),
    path("blog/", include("apps.blog.urls")),
    path("gallery/", include("apps.gallery.urls")),
    path("", include("apps.core.urls")),
]

if not settings.USE_S3:
    # django.conf.urls.static.static() is a no-op whenever DEBUG=False, so it
    # can't be used to serve user-uploaded media in production. This project
    # has no CDN/S3 in front of it, so serve media directly from Django/gunicorn
    # (fine at this traffic scale; switch to USE_S3 if that changes).
    urlpatterns += [
        re_path(r"^%s(?P<path>.*)$" % re.escape(settings.MEDIA_URL.lstrip("/")), serve_static, {"document_root": settings.MEDIA_ROOT}),
    ]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS[0])

handler404 = "apps.core.error_views.custom_404"
handler500 = "apps.core.error_views.custom_500"
