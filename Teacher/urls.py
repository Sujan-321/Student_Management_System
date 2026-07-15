from django.urls import path
from . import views

urlpatterns = [
    path("dashboard/", views.TeacherDashboardView.as_view(), name="teacher_dashboard"),
    path("profile/", views.TeacherProfileView.as_view(), name="teacher_profile"),
]