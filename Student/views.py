from django.urls import reverse_lazy
from django.views.generic import *

from .forms import StudentForm
from .models import Student


class StudentListView(ListView):

    model = Student
    template_name = "Student/student_list.html"
    context_object_name = "students"
    paginate_by = 10
    ordering = ["id"]


class StudentCreateView(CreateView):

    model = Student
    form_class = StudentForm
    template_name = "Student/student_create.html"
    success_url = reverse_lazy("student_list")


class StudentUpdateView(UpdateView):

    model = Student
    form_class = StudentForm
    template_name = "Student/student_update.html"
    success_url = reverse_lazy("student_list")


class StudentDetailView(DetailView):

    model = Student
    template_name = "Student/student_detail.html"
    context_object_name = "student"


class StudentDeleteView(DeleteView):

    model = Student
    template_name = "Student/student_delete.html"
    success_url = reverse_lazy("student_list")