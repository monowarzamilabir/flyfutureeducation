from itertools import chain

from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from django.db.models import Prefetch
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.views.generic import DetailView, ListView, TemplateView, View

from apps.blog.models import Post
from apps.destinations.models import Country
from apps.scholarships.models import Scholarship
from apps.services.models import Service
from apps.team.models import Consultant

from .forms import JobApplicationForm
from .models import (
    FAQ,
    Benefit,
    FAQCategory,
    JobPosting,
    ProcessStep,
    SiteSettings,
    SiteStat,
    StaticPage,
    Testimonial,
)


class HomeView(TemplateView):
    template_name = "core/home.html"

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx.update(
            {
                "meta_title": SiteSettings.load().default_meta_title,
                "meta_description": SiteSettings.load().default_meta_description,
                "services": Service.objects.filter(is_featured=True)[:8] or Service.objects.all()[:8],
                "destinations": Country.objects.filter(is_featured=True)[:8] or Country.objects.all()[:8],
                "destinations_count": Country.objects.count(),
                "process_steps": ProcessStep.objects.all()[:4],
                "benefits": Benefit.objects.all()[:6],
                "team": Consultant.objects.filter(is_active=True)[:4],
                "testimonials": Testimonial.objects.filter(is_featured=True)[:6],
                "stats": SiteStat.objects.all()[:4],
                "scholarships": Scholarship.objects.filter(is_featured=True)[:3],
                "latest_posts": Post.objects.filter(is_published=True)[:3],
            }
        )
        return ctx


class AboutView(TemplateView):
    template_name = "core/about.html"

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx.update(
            {
                "meta_title": "About Us | Fly Future Education",
                "meta_description": "Learn about Fly Future Education's mission, values, and the expert team helping Bangladeshi students study abroad.",
                "benefits": Benefit.objects.all(),
                "stats": SiteStat.objects.all(),
                "team": Consultant.objects.filter(is_active=True),
            }
        )
        return ctx


class TestimonialListView(ListView):
    model = Testimonial
    template_name = "core/testimonials.html"
    context_object_name = "testimonials"
    paginate_by = 12

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["meta_title"] = "Student Testimonials | Fly Future Education"
        ctx["meta_description"] = "Read real success stories from students Fly Future Education has helped study abroad."
        return ctx


class FAQView(TemplateView):
    template_name = "core/faq.html"

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx.update(
            {
                "meta_title": "Frequently Asked Questions | Fly Future Education",
                "meta_description": "Answers to common questions about visas, admissions, and scholarships from Fly Future Education.",
                "categories": FAQCategory.objects.prefetch_related(
                    Prefetch("faqs", queryset=FAQ.objects.filter(is_published=True))
                ).all(),
            }
        )
        return ctx


class CareerListView(ListView):
    model = JobPosting
    template_name = "core/careers.html"
    context_object_name = "jobs"

    def get_queryset(self):
        return JobPosting.objects.filter(is_active=True)

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["meta_title"] = "Careers | Fly Future Education"
        ctx["meta_description"] = "Join the Fly Future Education team. View current job openings in Dhaka."
        return ctx


class CareerDetailView(View):
    template_name = "core/career_detail.html"

    def get(self, request, slug):
        job = get_object_or_404(JobPosting, slug=slug, is_active=True)
        form = JobApplicationForm()
        return render(request, self.template_name, self._context(job, form))

    def post(self, request, slug):
        job = get_object_or_404(JobPosting, slug=slug, is_active=True)
        form = JobApplicationForm(request.POST, request.FILES)
        if form.is_valid():
            application = form.save(commit=False)
            application.job = job
            application.save()
            send_mail(
                subject=f"New job application: {job.title}",
                message=(
                    f"{application.full_name} applied for {job.title}.\n"
                    f"Email: {application.email}\nPhone: {application.phone}\n\n{application.cover_note}"
                ),
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[settings.ADMIN_NOTIFICATION_EMAIL],
                fail_silently=True,
            )
            messages.success(request, "Your application has been submitted. We'll be in touch soon!")
            return redirect("core:career_detail", slug=slug)
        return render(request, self.template_name, self._context(job, form))

    def _context(self, job, form):
        return {
            "job": job,
            "form": form,
            "meta_title": job.meta_title or f"{job.title} | Careers at Fly Future Education",
            "meta_description": job.meta_description,
        }


class StaticPageView(DetailView):
    model = StaticPage
    template_name = "core/static_page.html"
    context_object_name = "page"
    slug_field = "slug"
    slug_url_kwarg = "slug"

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        page = ctx["page"]
        ctx["meta_title"] = page.meta_title or page.title
        ctx["meta_description"] = page.meta_description
        return ctx


class SearchView(TemplateView):
    template_name = "core/search_results.html"

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        query = self.request.GET.get("q", "").strip()
        services, posts = [], []
        if query:
            services = Service.objects.filter(title__icontains=query) | Service.objects.filter(
                short_description__icontains=query
            )
            posts = Post.objects.filter(is_published=True).filter(title__icontains=query)
        ctx.update(
            {
                "query": query,
                "services": services.distinct() if query else [],
                "posts": posts.distinct() if query else [],
                "meta_title": f"Search results for '{query}'" if query else "Search",
            }
        )
        return ctx
