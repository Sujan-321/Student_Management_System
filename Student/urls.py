from django.urls import path

from .views import (
    AttendanceListView,
    AttendanceCreateView,
    AttendanceUpdateView,
    AttendanceDetailView,
    AttendanceReportView,
    MarkListView,
    MarkCreateView,
    MarkUpdateView,
    ResultSheetView,
    TranscriptView,
    ExamListView,
    ExamCreateView,
    ExamUpdateView,
    ClassRoomCreateView,
    ClassRoomListView,
    ClassRoomUpdateView,
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
    path(
        "exam/",
        ExamListView.as_view(),
        name="exam_list",
    ),

    path(
        "exam/create/",
        ExamCreateView.as_view(),
        name="exam_create",
    ),

    path(
        "exam/<int:pk>/update/",
        ExamUpdateView.as_view(),
        name="exam_update",
    ),
    path(
        "classrooms/",
        ClassRoomListView.as_view(),
        name="classroom_list",
    ),

    path(
        "classrooms/create/",
        ClassRoomCreateView.as_view(),
        name="classroom_create",
    ),

    path(
        "classrooms/<int:pk>/update/",
        ClassRoomUpdateView.as_view(),
        name="classroom_update",
    ),

]