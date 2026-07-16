from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.views.generic import TemplateView, UpdateView, ListView, CreateView, DeleteView, DetailView
from django.urls import reverse_lazy
from .forms import TeacherProfileForm, AssignmentForm, StudentForm, AttendanceForm, MarkForm, ExamForm, AssignmentSubmissionForm
from .models import Teacher, Subject, Post
from Student.models import Student
from django.contrib import messages
from django.shortcuts import redirect
from django import forms
from django.db.models import Q, Count
from django.shortcuts import get_object_or_404
from django.http import Http404
from Student.models import Attendance, Mark, Exam, AssignmentSubmission, ClassRoom
from Student.forms import ClassRoomForm




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


class TeacherProfileView(LoginRequiredMixin, UpdateView):

    model = Teacher
    form_class = TeacherProfileForm
    template_name = "Teacher/profile.html"
    success_url = reverse_lazy("teacher_profile")

    def get_object(self):

        return Teacher.objects.get(user=self.request.user)

# working for Assignment
class AssignmentListView(LoginRequiredMixin, ListView):
    model = Post
    template_name = "Teacher/assignment/assignment_list.html"
    context_object_name = "assignments"
    ordering = ["-created_at"]

    def get_queryset(self):
        teacher = Teacher.objects.get(user=self.request.user)
        return Post.objects.filter(teacher=teacher).order_by("-created_at")

class AssignmentCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):

    permission_required = "Teacher.add_post"

    model = Post
    form_class = AssignmentForm
    template_name = "Teacher/assignment/assignment_create.html"
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
    template_name = "Teacher/assignment/assignment_update.html"
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


# working on student feature
class StudentListView(LoginRequiredMixin, ListView):
    model = Student
    template_name = "Teacher/student_list.html"
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
                Q(registration_no__icontains=search)
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
    template_name = "Teacher/student_update.html"
    success_url = reverse_lazy("student_list")

    def form_valid(self, form):

        messages.success(self.request, "Student updated successfully.")

        return super().form_valid(form)

class StudentDetailView(LoginRequiredMixin, DetailView):

    model = Student
    template_name = "Teacher/student_detail.html"
    context_object_name = "student"

    def get_object(self):

        obj = super().get_object()

        user = self.request.user

        # Student can only view their own record
        if hasattr(user, "student_profile"):

            if obj != user.student_profile:
                raise Http404("You cannot view another student's profile.")

        return obj


# working on Attendance
class AttendanceListView(LoginRequiredMixin, ListView):
    """
    Display all attendance records.
    """

    model = Attendance
    template_name = "Teacher/attendance/attendance_list.html"
    context_object_name = "attendances"
    ordering = ["-attendance_date", "student"]
    paginate_by = 10

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
    template_name = "Teacher/attendance/attendance_create.html"
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
    template_name = "Teacher/attendance/attendance_update.html"
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
    template_name = "Teacher/attendance/attendance_detail.html"
    context_object_name = "attendance"

class AttendanceReportView(TemplateView):
    """
    Display attendance summary grouped by student and subject.
    """

    template_name = "Teacher/attendance/attendance_report.html"

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


# working on Mark, result, and transcript
class MarkListView(LoginRequiredMixin, ListView):
    """
    Display all student marks.
    """

    model = Mark
    template_name = "Teacher/marks/mark_list.html"
    context_object_name = "marks"
    ordering = [
        "student__first_name",
        "subject__sub_name",
    ]
    paginate_by = 10

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
    template_name = "Teacher/marks/mark_create.html"
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
    template_name = "Teacher/marks/mark_update.html"
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

    template_name = "Teacher/marks/result_sheet.html"

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

    template_name = "Teacher/marks/transcript.html"

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
    template_name = "Teacher/exam/exam_list.html"
    context_object_name = "exams"
    ordering = [
        "-start_date",
        "exam_name",
    ]
    paginate_by = 10

class ExamCreateView(CreateView):
    """
    Create a new examination.
    """

    model = Exam
    form_class = ExamForm
    template_name = "Teacher/exam/exam_create.html"
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
    template_name = "Teacher/exam/exam_update.html"
    success_url = reverse_lazy("exam_list")

    def form_valid(self, form):
        messages.success(
            self.request,
            "Examination updated successfully."
        )
        return super().form_valid(form)



 #working on classroom feature
class ClassRoomListView(ListView):
    """
    Display a list of all classrooms.
    """

    model = ClassRoom
    template_name = "Teacher/classroom/classroom_list.html"
    context_object_name = "classrooms"
    ordering = [
        "name",
        "section",
    ]
    paginate_by = 10


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
    template_name = "classroom/classroom_update.html"
    success_url = reverse_lazy("classroom_list")

    def form_valid(self, form):
        messages.success(
            self.request,
            "Classroom updated successfully."
        )
        return super().form_valid(form)

