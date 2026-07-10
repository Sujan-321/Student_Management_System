# from django.urls import reverse_lazy
# from django.views.generic import *

# from .forms import StudentForm
# from .models import Student


# class StudentListView(ListView):

#     model = Student
#     template_name = "Student/student_list.html"
#     context_object_name = "students"
#     paginate_by = 10
#     ordering = ["id"]


# class StudentCreateView(CreateView):

#     model = Student
#     form_class = StudentForm
#     template_name = "Student/student_create.html"
#     success_url = reverse_lazy("student_list")


# class StudentUpdateView(UpdateView):

#     model = Student
#     form_class = StudentForm
#     template_name = "Student/student_update.html"
#     success_url = reverse_lazy("student_list")


# class StudentDetailView(DetailView):

#     model = Student
#     template_name = "Student/student_detail.html"
#     context_object_name = "student"


# class StudentDeleteView(DeleteView):

#     model = Student
#     template_name = "Student/student_delete.html"
#     success_url = reverse_lazy("student_list")






from django.contrib import messages
from django.db.models import Q
from django.urls import reverse_lazy
from django.views.generic import *

from .forms import StudentForm, DepartmentForm
from .models import Student, Department


class StudentListView(ListView):

    model = Student
    template_name = "Student/student_list.html"
    context_object_name = "students"
    paginate_by = 10

    def get_queryset(self):

        queryset = Student.objects.all().order_by("roll_number")

        search = self.request.GET.get("search")

        department = self.request.GET.get("department")

        status = self.request.GET.get("status")

        if search:

            queryset = queryset.filter(

                Q(first_name__icontains=search) |
                Q(last_name__icontains=search) |
                Q(roll_number__icontains=search) |
                Q(registration_number__icontains=search)

            )

        if department:

            queryset = queryset.filter(department_id=department)

        if status:

            queryset = queryset.filter(status=status)

        return queryset


class StudentCreateView(CreateView):

    model = Student
    form_class = StudentForm
    template_name = "Student/student_create.html"
    success_url = reverse_lazy("student_list")

    def form_valid(self, form):

        messages.success(self.request, "Student added successfully.")

        return super().form_valid(form)


class StudentUpdateView(UpdateView):

    model = Student
    form_class = StudentForm
    template_name = "Student/student_update.html"
    success_url = reverse_lazy("student_list")

    def form_valid(self, form):

        messages.success(self.request, "Student updated successfully.")

        return super().form_valid(form)


class StudentDetailView(DetailView):

    model = Student
    template_name = "Student/student_detail.html"
    context_object_name = "student"


class StudentDeleteView(DeleteView):

    model = Student
    template_name = "Student/student_delete.html"
    success_url = reverse_lazy("student_list")

    def form_valid(self, form):

        messages.success(self.request, "Student deleted successfully.")

        return super().form_valid(form)



class DepartmentListView(ListView):
    model = Department
    template_name = "Student/department/department_list.html"
    context_object_name = "departments"
    ordering = ["name"]


class DepartmentCreateView(CreateView):
    model = Department
    form_class = DepartmentForm
    template_name = "Student/department/department_create.html"
    success_url = reverse_lazy("department_list")

    def form_valid(self, form):
        messages.success(
            self.request,
            "Department created successfully."
        )
        return super().form_valid(form)


class DepartmentUpdateView(UpdateView):
    model = Department
    form_class = DepartmentForm
    template_name = "Student/department/department_update.html"
    success_url = reverse_lazy("department_list")

    def form_valid(self, form):
        messages.success(
            self.request,
            "Department updated successfully."
        )
        return super().form_valid(form)