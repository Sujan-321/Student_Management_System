from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView, UpdateView
from django.urls import reverse_lazy

from .forms import TeacherProfileForm
from .models import Teacher


class TeacherDashboardView(LoginRequiredMixin, TemplateView):

    template_name = "Teacher/dashboard.html"

    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)

        context["teacher"] = Teacher.objects.get(user=self.request.user)

        context["student_count"] = 0
        context["class_count"] = 0
        context["subject_count"] = 0

        return context


class TeacherProfileView(LoginRequiredMixin, UpdateView):

    model = Teacher
    form_class = TeacherProfileForm
    template_name = "Teacher/profile.html"
    success_url = reverse_lazy("teacher_profile")

    def get_object(self):

        return Teacher.objects.get(user=self.request.user)