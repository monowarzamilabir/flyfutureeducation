from django.contrib.sitemaps import Sitemap
from django.urls import reverse

from apps.blog.models import Post
from apps.destinations.models import Country
from apps.scholarships.models import Scholarship
from apps.services.models import Service
from apps.team.models import Consultant
from apps.trainings.models import TestPrepCourse


class StaticViewSitemap(Sitemap):
    priority = 0.6
    changefreq = "monthly"

    def items(self):
        return [
            "core:home",
            "core:about",
            "services:list",
            "destinations:list",
            "scholarships:list",
            "trainings:list",
            "team:list",
            "applications:apply",
            "contact:contact",
            "blog:list",
            "gallery:albums",
            "gallery:videos",
            "core:testimonials",
            "core:faq",
            "core:careers",
        ]

    def location(self, item):
        return reverse(item)


class ServiceSitemap(Sitemap):
    changefreq = "monthly"
    priority = 0.8

    def items(self):
        return Service.objects.all()

    def lastmod(self, obj):
        return obj.updated_at


class CountrySitemap(Sitemap):
    changefreq = "monthly"
    priority = 0.9

    def items(self):
        return Country.objects.all()

    def lastmod(self, obj):
        return obj.updated_at


class ScholarshipSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.7

    def items(self):
        return Scholarship.objects.all()

    def lastmod(self, obj):
        return obj.updated_at


class TestPrepCourseSitemap(Sitemap):
    changefreq = "monthly"
    priority = 0.6

    def items(self):
        return TestPrepCourse.objects.all()

    def lastmod(self, obj):
        return obj.updated_at


class ConsultantSitemap(Sitemap):
    changefreq = "monthly"
    priority = 0.4

    def items(self):
        return Consultant.objects.filter(is_active=True)


class BlogPostSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.6

    def items(self):
        return Post.objects.filter(is_published=True)

    def lastmod(self, obj):
        return obj.updated_at
