from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView, UpdateView
from django.urls import reverse_lazy

from .models import Teacher
from .forms import TeacherProfileForm


class TeacherDashboardView(LoginRequiredMixin, TemplateView):
    template_name = "Teacher/dashboard.html"


class TeacherProfileView(LoginRequiredMixin, UpdateView):
    model = Teacher
    form_class = TeacherProfileForm
    template_name = "Teacher/profile.html"
    success_url = reverse_lazy("teacher_profile")

    def get_object(self):
        return Teacher.objects.get(user=self.request.user)