from django.views.generic import DetailView, ListView

from .models import TestPrepCourse


class CourseListView(ListView):
    model = TestPrepCourse
    template_name = "trainings/course_list.html"
    context_object_name = "courses"
    paginate_by = 12

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["meta_title"] = "Test Prep & Coaching | Fly Future Education"
        ctx["meta_description"] = "IELTS, TOEFL, PTE, and Duolingo English Test coaching from Fly Future Education, with schedules and fees."
        return ctx


class CourseDetailView(DetailView):
    model = TestPrepCourse
    template_name = "trainings/course_detail.html"
    context_object_name = "course"

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        course = ctx["course"]
        ctx["meta_title"] = course.meta_title or f"{course.title} | Fly Future Education"
        ctx["meta_description"] = course.meta_description or course.short_description
        return ctx
