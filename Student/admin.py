from django.contrib import admin

from .models import Student, Department


@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "code",
    )

    search_fields = (
        "name",
        "code",
    )


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):

    list_display = (
        "rank",
        "first_name",
        "last_name",
        "department",
        "contact",
        "status",
    )

    list_filter = (
        "department",
        "gender",
        "status",
    )

    search_fields = (
        "first_name",
        "last_name",
        "rank",
        "registration_number",
    )