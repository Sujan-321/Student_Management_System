from django.urls import reverse_lazy
from django.views.generic import *

from .forms import StudentForm
from .models import Student


class StudentCreateView(CreateView):

    model = Student
    form_class = StudentForm
    template_name = "Student/student_create.html"
    success_url = reverse_lazy("student_list")


