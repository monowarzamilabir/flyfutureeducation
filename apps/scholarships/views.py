from django.views.generic import DetailView, ListView

from .models import Scholarship


class ScholarshipListView(ListView):
    model = Scholarship
    template_name = "scholarships/scholarship_list.html"
    context_object_name = "scholarships"
    paginate_by = 12

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["meta_title"] = "Scholarships | Fly Future Education"
        ctx["meta_description"] = "Discover scholarship opportunities for studying abroad, curated by Fly Future Education."
        return ctx


class ScholarshipDetailView(DetailView):
    model = Scholarship
    template_name = "scholarships/scholarship_detail.html"
    context_object_name = "scholarship"

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        scholarship = ctx["scholarship"]
        ctx["meta_title"] = scholarship.meta_title or f"{scholarship.title} | Fly Future Education"
        ctx["meta_description"] = scholarship.meta_description or scholarship.amount_coverage
        return ctx
