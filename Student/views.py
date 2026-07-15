<<<<<<< HEAD
=======
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






>>>>>>> 0f13a1315549bf8329c66abfbbfc12654dfa0b16
from django.contrib import messages
from django.db.models import Q, Count
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DetailView, TemplateView, DeleteView
from .forms import StudentForm, DepartmentForm, AttendanceForm, MarkForm, ExamForm, ClassRoomForm
from .models import Student, Department, Attendance, Mark, Exam, ClassRoom, Teacher
from django.shortcuts import get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.http import Http404


class StudentDashboardView(LoginRequiredMixin, TemplateView):

    template_name = "Student/dashboard.html"

    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)

        student = Student.objects.filter(user=self.request.user).first()

        context["student"] = student

        context["attendance_count"] = (
            Attendance.objects.filter(student=student).count()
            if student else 0
        )

        context["mark_count"] = (
            Mark.objects.filter(student=student).count()
            if student else 0
        )

        context["exam_count"] = Exam.objects.count()

        context["teacher_count"] = Teacher.objects.count()

        return context

class StudentProfileView(LoginRequiredMixin, DetailView):

    model = Student
    template_name = "Student/profile.html"
    context_object_name = "student"

    def get_object(self):

        try:
            return Student.objects.get(user=self.request.user)

        except Student.DoesNotExist:
            raise Http404("Student profile not found.")


class StudentProfileUpdateView(LoginRequiredMixin, UpdateView):

    model = Student
    form_class = StudentForm
    template_name = "Student/profile_update.html"
    success_url = reverse_lazy("student_profile")

    def get_object(self):

        return Student.objects.get(user=self.request.user)

    def form_valid(self, form):

        messages.success(
            self.request,
            "Profile updated successfully."
        )

        return super().form_valid(form)
    


class StudentListView(LoginRequiredMixin, ListView):

    model = Student
    template_name = "Student/student_list.html"
    context_object_name = "students"
    paginate_by = 10

    def get_queryset(self):

        queryset = Student.objects.all().order_by("rank")

        search = self.request.GET.get("search")

        department = self.request.GET.get("department")

        status = self.request.GET.get("status")

        if search:

            queryset = queryset.filter(

                Q(first_name__icontains=search) |
                Q(last_name__icontains=search) |
                Q(rank__icontains=search) |
                Q(registration_number__icontains=search)

            )

        if department:

            queryset = queryset.filter(department_id=department)

        if status:

            queryset = queryset.filter(status=status)

        return queryset


class StudentCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):  # only teacher can create student

    permission_required = "Student.add_student"

    model = Student
    form_class = StudentForm
    template_name = "Student/student_create.html"
    success_url = reverse_lazy("student_list")

    def form_valid(self, form):

        messages.success(self.request, "Student added successfully.")

        return super().form_valid(form)


class StudentUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):

    permission_required = "Student.change_student"

    model = Student
    form_class = StudentForm
    template_name = "Student/student_update.html"
    success_url = reverse_lazy("student_list")

    def form_valid(self, form):

        messages.success(self.request, "Student updated successfully.")

        return super().form_valid(form)


class StudentDetailView(LoginRequiredMixin, DetailView):

    model = Student
    template_name = "Student/student_detail.html"
    context_object_name = "student"

    def get_object(self):

        obj = super().get_object()

        user = self.request.user

        # Student can only view their own record
        if hasattr(user, "student_profile"):

            if obj != user.student_profile:
                raise Http404("You cannot view another student's profile.")

        return obj


class StudentDeleteView(DeleteView):

    model = Student
    template_name = "Student/student_delete.html"
    success_url = reverse_lazy("student_list")

    def form_valid(self, form):

        messages.success(self.request, "Student deleted successfully.")

        return super().form_valid(form)


# working on Department feature

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


# working on attendance

class AttendanceListView(LoginRequiredMixin, ListView):
    """
    Display all attendance records.
    """

    model = Attendance
    template_name = "attendance/attendance_list.html"
    context_object_name = "attendances"
    ordering = ["-attendance_date", "student"]

    def get_queryset(self):

        queryset = Attendance.objects.select_related(
            "student",
            "teacher",
            "subject",
        )

        user = self.request.user

        # Student
        if hasattr(user, "student_profile"):
            return queryset.filter(student=user.student_profile)

        # Teacher / Admin
        return queryset


class AttendanceCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):

    permission_required = "Student.add_attendance"

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

class MarkListView(LoginRequiredMixin, ListView):
    """
    Display all student marks.
    """

    model = Mark
    template_name = "marks/mark_list.html"
    context_object_name = "marks"
    ordering = [
        "student__first_name",
        "subject__sub_name",
    ]

    def get_queryset(self):

        queryset = Mark.objects.select_related(
            "student",
            "teacher",
            "subject",
            "exam",
        )

        user = self.request.user

        if hasattr(user, "student_profile"):
            return queryset.filter(student=user.student_profile)

        return queryset


class MarkCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    permission_required = "Student.add_mark"

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


class ResultSheetView(LoginRequiredMixin, PermissionRequiredMixin, TemplateView):
    """
    Display the result sheet of a selected exam.
    """

    permission_required = "Student.view_mark"

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


class TranscriptView(LoginRequiredMixin, TemplateView):
    """
    Display the complete academic transcript of a student.
    """

    template_name = "Student/marks/transcript.html"

    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)

        user = self.request.user

        # Student can view only own transcript
        if hasattr(user, "student_profile"):

            student = user.student_profile

        else:

            student = get_object_or_404(
                Student,
                pk=self.kwargs["student_id"],
            )

        marks = (
            Mark.objects.filter(student=student)
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
    template_name = "exam/exam_list.html"
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



# working on classroom feature
class ClassRoomListView(ListView):
    """
    Display a list of all classrooms.
    """

    model = ClassRoom
    template_name = "classroom/classroom_list.html"
    context_object_name = "classrooms"
    ordering = [
        "name",
        "section",
    ]


class ClassRoomCreateView(CreateView):
    """
    Create a new classroom.
    """

    model = ClassRoom
    form_class = ClassRoomForm
    template_name = "classroom/classroom_create.html"
    success_url = reverse_lazy("classroom_list")

    def form_valid(self, form):
        messages.success(
            self.request,
            "Classroom created successfully."
        )
        return super().form_valid(form)


class ClassRoomUpdateView(UpdateView):
    """
    Update an existing classroom.
    """

    model = ClassRoom
    form_class = ClassRoomForm
    template_name = "Student/classroom/classroom_update.html"
    success_url = reverse_lazy("classroom_list")

    def form_valid(self, form):
        messages.success(
            self.request,
            "Classroom updated successfully."
        )
        return super().form_valid(form)