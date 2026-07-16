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

from .views import (
    
    # for student
    StudentListView,
    StudentCreateView,
    StudentUpdateView,
    StudentDetailView,

    #for attendance
    AttendanceListView,
    AttendanceCreateView,
    AttendanceUpdateView,
    AttendanceDetailView,
    AttendanceReportView,

    # for marks
    MarkListView,
    MarkCreateView,
    MarkUpdateView,

    # for result
    ResultSheetView,
    TranscriptView,

    # for exam
    ExamListView,
    ExamCreateView,
    ExamUpdateView,

    #for assignment
    AssignmentListView,
    AssignmentSubmitView,
)

urlpatterns = [

    # for student feature
    path("student-list/", StudentListView.as_view(), name="student_list"),
    path("student-create/", StudentCreateView.as_view(), name="student_create"),
    path("student-update/<int:pk>/", StudentUpdateView.as_view(), name="student_update"),
    path("student-detail/<int:pk>/", StudentDetailView.as_view(), name="student_detail"),


    # for attendance
    path("attendance/", AttendanceListView.as_view(), name="attendance_list"),
    path("attendance/create/", AttendanceCreateView.as_view(), name="attendance_create"),
    path("attendance/<int:pk>/update/", AttendanceUpdateView.as_view(), name="attendance_update"),
    path("attendance/<int:pk>/", AttendanceDetailView.as_view(), name="attendance_detail"),
    path("attendance/report/", AttendanceReportView.as_view(), name="attendance_report"),

    # for marks
    path("marks/", MarkListView.as_view(), name="mark_list"),
    path("marks/create/", MarkCreateView.as_view(), name="mark_create"),
    path("marks/<int:pk>/update/", MarkUpdateView.as_view(), name="mark_update"),
    path("marks/result-sheet/<int:exam_id>/", ResultSheetView.as_view(), name="result_sheet"),
    path("marks/transcript/<int:student_id>/", TranscriptView.as_view(), name="transcript"),

    # for exam
    path("exam/", ExamListView.as_view(), name="exam_list"),
    path("exam/create/", ExamCreateView.as_view(), name="exam_create"),
    path("exam/<int:pk>/update/", ExamUpdateView.as_view(), name="exam_update"),

    path("assignments/", AssignmentListView.as_view(), name="assignment_list"),
    path("assignment/<int:pk>/submit/", AssignmentSubmitView.as_view(), name="assignment_submit"),

]