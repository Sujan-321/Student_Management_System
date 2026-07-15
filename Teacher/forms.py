from django import forms
from .models import Teacher


class TeacherProfileForm(forms.ModelForm):
    class Meta:
        model = Teacher
        exclude = ("user",)

from django import forms
from .models import Post


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