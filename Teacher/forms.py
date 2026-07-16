from django import forms
from .models import Teacher, Post
from Student.models import Student, Department, ClassRoom, Attendance, Exam, Mark, AssignmentSubmission


class TeacherProfileForm(forms.ModelForm):
    class Meta:
        model = Teacher
        exclude = ("user",)

class AssignmentForm(forms.ModelForm):

    class Meta:

        model = Post

        fields = [
            "title",
            "desc",
        ]

        widgets = {
            "title": forms.TextInput(
                attrs={"class": "form-control"}
            ),
            "desc": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 5,
                }
            ),
        }



class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        exclude = ("created_at", "updated_at")



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