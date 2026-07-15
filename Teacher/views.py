from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.views.generic import TemplateView, UpdateView, ListView, CreateView, DeleteView
from django.urls import reverse_lazy
from .forms import TeacherProfileForm, AssignmentForm
from .models import Teacher, Subject, Post
from Student.models import Student
from django.contrib import messages
from django.shortcuts import redirect
from django import forms


class TeacherDashboardView(LoginRequiredMixin, TemplateView):

    template_name = "Teacher/dashboard.html"

    def dispatch(self, request, *args, **kwargs):

        if not request.user.groups.filter(name="Teacher").exists():

            messages.error(
                request,
                "Only teachers can access this page."
            )

            return redirect("home")

        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)

        teacher = Teacher.objects.get(user=self.request.user)

        context["teacher"] = teacher
        context["student_count"] = Student.objects.count()
        context["teacher_count"] = Teacher.objects.count()
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




class AssignmentListView(LoginRequiredMixin, ListView):
    model = Post
    template_name = "Teacher/assignment_list.html"
    context_object_name = "assignments"
    ordering = ["-created_at"]

    def get_queryset(self):
        teacher = Teacher.objects.get(user=self.request.user)
        return Post.objects.filter(teacher=teacher).order_by("-created_at")


class AssignmentCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):

    permission_required = "Teacher.add_post"

    model = Post
    form_class = AssignmentForm
    template_name = "Teacher/assignment_create.html"
    success_url = reverse_lazy("assignment_list")

    def form_valid(self, form):

        form.instance.teacher = Teacher.objects.get(
            user=self.request.user
        )

        messages.success(
            self.request,
            "Assignment created successfully."
        )

        return super().form_valid(form)

class AssignmentUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):

    permission_required = "Teacher.change_post"

    model = Post
    form_class = AssignmentForm
    template_name = "Teacher/assignment_update.html"
    success_url = reverse_lazy("assignment_list")

    def form_valid(self, form):

        messages.success(
            self.request,
            "Assignment updated successfully."
        )

        return super().form_valid(form)

class AssignmentDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):

    permission_required = "Teacher.delete_post"

    model = Post
    template_name = "Teacher/assignment_delete.html"
    success_url = reverse_lazy("assignment_list")

    def form_valid(self, form):

        messages.success(
            self.request,
            "Assignment deleted successfully."
        )

        return super().form_valid(form)



