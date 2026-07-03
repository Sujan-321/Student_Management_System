from django.contrib import messages
from django.contrib.auth.models import User
from django.urls import reverse_lazy
from django.views.generic import CreateView
from django.contrib.auth.views import LoginView

from .forms import UserRegistrationForm, UserLoginForm


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




class UserLoginView(LoginView):
    template_name = "accounts/login.html"
    authentication_form = UserLoginForm

    def form_valid(self, form):
        remember_me = form.cleaned_data.get("remember_me")

        if not remember_me:
            self.request.session.set_expiry(0)

        messages.success(self.request, "Logged in successfully.")

        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy("home")