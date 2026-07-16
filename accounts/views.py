from django.contrib import messages
from django.contrib.auth.models import User
from django.urls import reverse_lazy
from django.views.generic import CreateView, TemplateView
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import logout
from django.views import View
from django.shortcuts import redirect


from django.contrib import messages
from django.contrib.auth.views import (
    PasswordChangeView,
    PasswordChangeDoneView,
    PasswordResetView,
    PasswordResetDoneView,
    PasswordResetConfirmView,
    PasswordResetCompleteView,
)

from .forms import UserRegistrationForm, UserLoginForm


class HomeView(TemplateView):
    template_name = "accounts/home.html"


class RegisterView(CreateView):
    model = User            # here we use 'USER' model
    form_class = UserRegistrationForm  
    template_name = "accounts/register.html"
    success_url = reverse_lazy("login")

    def form_valid(self, form):
        response = super().form_valid(form)

        messages.success(
            self.request,
            "Your account has been created successfully. Please log in."
        )

        return response


class DeactivateAccountView(LoginRequiredMixin, View):

    def post(self, request):

        user = request.user

        user.is_active = False

        user.save()

        logout(request)

        messages.success(
            request,
            "Your account has been deactivated."
        )

        return redirect("home")

class UserLoginView(LoginView):
    template_name = "accounts/login.html"
    authentication_form = UserLoginForm

    def form_valid(self, form):
        remember_me = form.cleaned_data.get("remember_me")

        if not remember_me:
            self.request.session.set_expiry(0)

        messages.success(self.request, "Logged in successfully.")

        return super().form_valid(form)

    # def get_success_url(self):
    #     return reverse_lazy("home")

    def get_success_url(self):

        user = self.request.user

        if user.is_superuser:
            return reverse_lazy("admin:index")

        if user.groups.filter(name="Teacher").exists():  # here we check the data is present in the Teacher 
            return reverse_lazy("teacher:teacher_dashboard")    # it render the user in the teacher urls.py file

        if user.groups.filter(name="Student").exists():
            return reverse_lazy("student_dashboard")

        return reverse_lazy("home")


class UserLogoutView(LogoutView):

    def dispatch(self, request, *args, **kwargs):
        messages.success(request, "Logged out successfully.")
        return super().dispatch(request, *args, **kwargs)


class UserPasswordChangeView(PasswordChangeView):
    template_name = "accounts/password_change.html"
    success_url = reverse_lazy("password_change_done")

    def form_valid(self, form):
        messages.success(self.request, "Password changed successfully.")
        return super().form_valid(form)


class UserPasswordChangeDoneView(PasswordChangeDoneView):
    template_name = "accounts/password_change_done.html"



class UserPasswordResetView(PasswordResetView):
    template_name = "accounts/password_reset.html"
    email_template_name = "accounts/password_reset_email.html"
    subject_template_name = "accounts/password_reset_subject.txt"
    success_url = reverse_lazy("password_reset_done")


class UserPasswordResetDoneView(PasswordResetDoneView):
    template_name = "accounts/password_reset_done.html"


class UserPasswordResetConfirmView(PasswordResetConfirmView):
    template_name = "accounts/password_reset_confirm.html"
    success_url = reverse_lazy("password_reset_complete")


class UserPasswordResetCompleteView(PasswordResetCompleteView):
    template_name = "accounts/password_reset_complete.html"