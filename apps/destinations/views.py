from django.views.generic import DetailView, ListView

from .models import Country


class CountryListView(ListView):
    model = Country
    template_name = "destinations/country_list.html"
    context_object_name = "countries"
    paginate_by = 12

    def get_queryset(self):
        qs = super().get_queryset()
        query = self.request.GET.get("q", "").strip()
        if query:
            qs = qs.filter(name__icontains=query)
        return qs

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["query"] = self.request.GET.get("q", "")
        ctx["meta_title"] = "Study Destinations | Fly Future Education"
        ctx["meta_description"] = "Browse study-abroad destinations supported by Fly Future Education, with visa requirements, costs, and intake seasons."
        return ctx


class CountryDetailView(DetailView):
    model = Country
    template_name = "destinations/country_detail.html"
    context_object_name = "country"

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        country = ctx["country"]
        ctx["meta_title"] = country.meta_title or f"Study in {country.name} | Fly Future Education"
        ctx["meta_description"] = country.meta_description or f"Everything you need to know about studying in {country.name}: visa requirements, costs, universities, and intake seasons."
        ctx["universities"] = country.universities.all()
        ctx["scholarships"] = country.scholarships.all()[:4]
        return ctx
