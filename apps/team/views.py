from django.views.generic import DetailView, ListView

from .models import Consultant


class ConsultantListView(ListView):
    model = Consultant
    template_name = "team/consultant_list.html"
    context_object_name = "consultants"

    def get_queryset(self):
        return Consultant.objects.filter(is_active=True)

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["meta_title"] = "Our Consultants | Fly Future Education"
        ctx["meta_description"] = "Meet the expert counsellors and visa consultants at Fly Future Education."
        return ctx


class ConsultantDetailView(DetailView):
    model = Consultant
    template_name = "team/consultant_detail.html"
    context_object_name = "consultant"

    def get_queryset(self):
        return Consultant.objects.filter(is_active=True)

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        consultant = ctx["consultant"]
        ctx["meta_title"] = f"{consultant.name} | Fly Future Education"
        ctx["meta_description"] = f"{consultant.name}, {consultant.designation} at Fly Future Education."
        return ctx
