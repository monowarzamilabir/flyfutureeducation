from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.contrib.sitemaps.views import sitemap
from django.urls import include, path
from django.views.generic import RedirectView, TemplateView

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

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS[0])

handler404 = "apps.core.error_views.custom_404"
handler500 = "apps.core.error_views.custom_500"
