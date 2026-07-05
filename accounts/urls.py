from django.urls import path

from .views import RegisterView, UserLogoutView, UserLoginView, HomeView, UserPasswordChangeView

urlpatterns = [
    path("", UserLoginView.as_view(), name="login"),
    path("/home", HomeView.as_view(), name="home"),
    path("login/", UserLoginView.as_view(), name="login"),
    path("register/", RegisterView.as_view(), name="register"),
    path("logout/", UserLogoutView.as_view(), name="logout"),
    path("password-change/", UserPasswordChangeView.as_view(), name="password_change"),
]