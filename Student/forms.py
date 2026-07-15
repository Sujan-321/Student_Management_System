from django import forms
from .models import Student, Department, ClassRoom, Attendance, Exam, Mark, AssignmentSubmission

class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        exclude = ("created_at", "updated_at")


class DepartmentForm(forms.ModelForm):

    class Meta:
        model = Department
        fields = "__all__"


class ClassRoomForm(forms.ModelForm):

    class Meta:
        model = ClassRoom
        fields = "__all__"


class ExamForm(forms.ModelForm):

    class Meta:
        model = Exam
        fields = "__all__"


class AttendanceForm(forms.ModelForm):

    class Meta:
        model = Attendance
        fields = "__all__"


class MarkForm(forms.ModelForm):

    class Meta:
        model = Mark
        fields = "__all__"
    

class AssignmentSubmissionForm(forms.ModelForm):

    class Meta:

        model = AssignmentSubmission

        fields = [
            "pdf",
        ]