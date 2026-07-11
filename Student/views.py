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
from django.db.models import Q, Count
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DetailView, TemplateView, DeleteView
from .forms import StudentForm, DepartmentForm, AttendanceForm, MarkForm, ExamForm
from .models import Student, Department, Attendance, Mark, Exam
from django.shortcuts import get_object_or_404




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


class AttendanceListView(ListView):
    """
    Display all attendance records.
    """

    model = Attendance
    template_name = "Student/attendance/attendance_list.html"
    context_object_name = "attendances"
    ordering = ["-attendance_date", "student"]


class AttendanceCreateView(CreateView):
    """
    Create a new attendance record.
    """

    model = Attendance
    form_class = AttendanceForm
    template_name = "Student/attendance/attendance_create.html"
    success_url = reverse_lazy("attendance_list")

    def form_valid(self, form):
        messages.success(
            self.request,
            "Attendance record has been created successfully."
        )
        return super().form_valid(form)


class AttendanceUpdateView(UpdateView):
    """
    Update an existing attendance record.
    """

    model = Attendance
    form_class = AttendanceForm
    template_name = "Student/attendance/attendance_update.html"
    success_url = reverse_lazy("attendance_list")

    def form_valid(self, form):
        messages.success(
            self.request,
            "Attendance record has been updated successfully."
        )
        return super().form_valid(form)


class AttendanceDetailView(DetailView):
    """
    Display detailed information for a single attendance record.
    """

    model = Attendance
    template_name = "Student/attendance/attendance_detail.html"
    context_object_name = "attendance"


class AttendanceReportView(TemplateView):
    """
    Display attendance summary grouped by student and subject.
    """

    template_name = "Student/attendance/attendance_report.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        reports = (
            Attendance.objects.values(
                "student__first_name",
                "student__last_name",
                "subject__sub_name",
            )
            .annotate(
                total=Count("id"),
                present=Count(
                    "id",
                    filter=Q(status="Present"),
                ),
                absent=Count(
                    "id",
                    filter=Q(status="Absent"),
                ),
                leave=Count(
                    "id",
                    filter=Q(status="Leave"),
                ),
            )
            .order_by(
                "student__first_name",
                "subject__sub_name",
            )
        )

        context["reports"] = reports

        return context



# here we start the marks features

class MarkListView(ListView):
    """
    Display all student marks.
    """

    model = Mark
    template_name = "Student/marks/mark_list.html"
    context_object_name = "marks"
    ordering = [
        "student__first_name",
        "subject__sub_name",
    ]


class MarkCreateView(CreateView):
    """
    Create a new mark entry.
    """

    model = Mark
    form_class = MarkForm
    template_name = "Student/marks/mark_create.html"
    success_url = reverse_lazy("mark_list")

    def form_valid(self, form):
        messages.success(
            self.request,
            "Marks added successfully."
        )
        return super().form_valid(form)


class MarkUpdateView(UpdateView):
    """
    Update an existing mark record.
    """

    model = Mark
    form_class = MarkForm
    template_name = "Student/marks/mark_update.html"
    success_url = reverse_lazy("mark_list")

    def form_valid(self, form):
        messages.success(
            self.request,
            "Marks updated successfully."
        )
        return super().form_valid(form)


class ResultSheetView(TemplateView):
    """
    Display the result sheet of a selected exam.
    """

    template_name = "Student/marks/result_sheet.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        exam_id = self.kwargs.get("exam_id")

        context["marks"] = (
            Mark.objects.filter(
                exam_id=exam_id
            )
            .select_related(
                "student",
                "subject",
                "exam",
            )
            .order_by(
                "student__first_name",
                "subject__sub_name",
            )
        )

        return context


class TranscriptView(TemplateView):
    """
    Display the complete academic transcript of a student.
    """

    template_name = "Student/marks/transcript.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        student = get_object_or_404(
            Student,
            pk=self.kwargs["student_id"],
        )

        marks = (
            Mark.objects.filter(
                student=student
            )
            .select_related(
                "subject",
                "exam",
                "teacher",
            )
            .order_by(
                "exam__start_date",
                "subject__sub_name",
            )
        )

        context["student"] = student
        context["marks"] = marks

        return context


# working on exam feature

class ExamListView(ListView):
    """
    Display a list of all examinations.
    """

    model = Exam
    template_name = "Student/exam/exam_list.html"
    context_object_name = "exams"
    ordering = [
        "-start_date",
        "exam_name",
    ]


class ExamCreateView(CreateView):
    """
    Create a new examination.
    """

    model = Exam
    form_class = ExamForm
    template_name = "Student/exam/exam_create.html"
    success_url = reverse_lazy("exam_list")

    def form_valid(self, form):
        messages.success(
            self.request,
            "Examination created successfully."
        )
        return super().form_valid(form)


class ExamUpdateView(UpdateView):
    """
    Update an existing examination.
    """

    model = Exam
    form_class = ExamForm
    template_name = "Student/exam/exam_update.html"
    success_url = reverse_lazy("exam_list")

    def form_valid(self, form):
        messages.success(
            self.request,
            "Examination updated successfully."
        )
        return super().form_valid(form)