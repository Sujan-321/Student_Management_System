from django.urls import path
from .views import TeacherDashboardView, TeacherProfileView, AssignmentListView, AssignmentCreateView, AssignmentUpdateView, AssignmentDeleteView

urlpatterns = [
    path("dashboard/", TeacherDashboardView.as_view(), name="teacher_dashboard"),
    path("profile/", TeacherProfileView.as_view(), name="teacher_profile"),
    path("assignments/", AssignmentListView.as_view(), name="assignment_list"),
    path("assignments/create/", AssignmentCreateView.as_view(), name="assignment_create"),
    path("assignments/<int:pk>/update/", AssignmentUpdateView.as_view(), name="assignment_update"),
    path("assignments/<int:pk>/delete/", AssignmentDeleteView.as_view(), name="assignment_delete"),
]