from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView, UpdateView
from django.urls import reverse_lazy

from .forms import TeacherProfileForm
from .models import Teacher, Subject
from Student.models import StudentProfile


class TeacherDashboardView(LoginRequiredMixin, TemplateView):

    template_name = "Teacher/dashboard.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context["teacher"] = Teacher.objects.get(user=self.request.user)
        context["student_count"] = StudentProfile.objects.count()
        # context["class_count"] = 0
        context["subject_count"] = Subject.objects.count()

        return context

# from django.http import Http404

# class TeacherDashboardView(LoginRequiredMixin, TemplateView):
#     template_name = "Teacher/dashboard.html"

#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)

#         print("=" * 50)
#         print("Logged in user:", self.request.user)
#         print("User ID:", self.request.user.id)
#         print("Username:", self.request.user.username)

#         teachers = Teacher.objects.filter(user=self.request.user)

#         print("Teacher queryset:", teachers)
#         print("Teacher count:", teachers.count())

#         if not teachers.exists():
#             raise Http404("No Teacher profile found for this user.")

#         context["teacher"] = teachers.first()
#         return context


class TeacherProfileView(LoginRequiredMixin, UpdateView):

    model = Teacher
    form_class = TeacherProfileForm
    template_name = "Teacher/profile.html"
    success_url = reverse_lazy("teacher_profile")

    def get_object(self):

        return Teacher.objects.get(user=self.request.user)