from django.urls import path

from .views import (
    AttendanceListView,
    AttendanceCreateView,
    AttendanceUpdateView,
    AttendanceDetailView,
    AttendanceReportView,
)

urlpatterns = [

    path(
        "attendance/",
        AttendanceListView.as_view(),
        name="attendance_list",
    ),

    path(
        "attendance/create/",
        AttendanceCreateView.as_view(),
        name="attendance_create",
    ),

    path(
        "attendance/<int:pk>/update/",
        AttendanceUpdateView.as_view(),
        name="attendance_update",
    ),

    path(
        "attendance/<int:pk>/",
        AttendanceDetailView.as_view(),
        name="attendance_detail",
    ),

    path(
        "attendance/report/",
        AttendanceReportView.as_view(),
        name="attendance_report",
    ),
]