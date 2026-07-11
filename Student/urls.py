from django.urls import path

from .views import AttendanceListView, AttendanceCreateView, AttendanceUpdateView, AttendanceDetailView, AttendanceReportView, MarkListView, MarkCreateView, MarkUpdateView, ResultSheetView, TranscriptView

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

    path(
        "marks/",
        MarkListView.as_view(),
        name="mark_list",
    ),

    path(
        "marks/create/",
        MarkCreateView.as_view(),
        name="mark_create",
    ),

    path(
        "marks/<int:pk>/update/",
        MarkUpdateView.as_view(),
        name="mark_update",
    ),

    path(
        "marks/result-sheet/<int:exam_id>/",
        ResultSheetView.as_view(),
        name="result_sheet",
    ),

    path(
        "marks/transcript/<int:student_id>/",
        TranscriptView.as_view(),
        name="transcript",
    ),

]