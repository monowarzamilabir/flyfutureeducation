from django.views.generic import DetailView, ListView

from .models import Service


class ServiceListView(ListView):
    model = Service
    template_name = "services/service_list.html"
    context_object_name = "services"
    paginate_by = 12

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["meta_title"] = "Our Services | Fly Future Education"
        ctx["meta_description"] = "Explore Fly Future Education's full range of study-abroad services: visa processing, admissions, scholarships, and more."
        return ctx


class ServiceDetailView(DetailView):
    model = Service
    template_name = "services/service_detail.html"
    context_object_name = "service"

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        service = ctx["service"]
        ctx["meta_title"] = service.meta_title or f"{service.title} | Fly Future Education"
        ctx["meta_description"] = service.meta_description or service.short_description
        ctx["related_services"] = Service.objects.exclude(pk=service.pk)[:3]
        ctx["whatsapp_message"] = f"Hi, I need help with {service.title}."
        return ctx
