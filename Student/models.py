from django.db import models
from django.conf import settings
from Teacher.models import Teacher, Subject, Post

class TimeStampModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

class Department(TimeStampModel):
    name = models.CharField(max_length=255, unique=True)
    code = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name
    

class ClassRoom(TimeStampModel):

    name = models.CharField(max_length=50)
    section = models.CharField(max_length=10)
    room_no = models.CharField(max_length=20)
    department = models.ForeignKey(
        Department,
        on_delete=models.CASCADE,
        related_name="classrooms"
    )

    class_teacher = models.ForeignKey(
        Teacher,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="class_teacher"
    )

    def __str__(self):
        return f"{self.name} ({self.section})"


class Student(TimeStampModel):
    GENDER_CHOICES = (
        ("Male", "Male"),
        ("Female", "Female"),
        ("Other", "Other"),
    )

    STATUS_CHOICES = (
        ("Active", "Active"),
        ("Inactive", "Inactive"),
    )

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="student_profile",
        null=True,
        blank=True
    )

    first_name = models.CharField(max_length=50, blank=True, null=True)
    last_name = models.CharField(max_length=50, null=True, blank=True)
    rank = models.CharField(max_length=20, unique=True)
    registration_no = models.CharField(max_length=20, unique=True)
    email = models.EmailField(unique=True)
    contact = models.CharField(max_length=15, unique=True)
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES)
    dob = models.DateField()
    address = models.TextField()
    guardian_name = models.CharField(max_length=100)
    guardian_phone = models.CharField(max_length=15)
    department = models.ForeignKey(Department, on_delete=models.CASCADE, related_name="students")
    admission_date = models.DateField()
    profile_image = models.ImageField(upload_to="Student/student_images/%Y/%m/%d/", blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="Active")    
    classroom = models.ForeignKey(ClassRoom, on_delete=models.CASCADE, related_name="students", null=True, blank=True)


    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class Attendance(TimeStampModel):

    STATUS_CHOICES = (
        ("Present", "Present"),
        ("Absent", "Absent"),
        ("Leave", "Leave"),
    )

    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name="attendance")
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE, related_name="attendance")
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name="attendance")
    attendance_date = models.DateField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES)
    remarks = models.CharField(max_length=200, blank=True)

    class Meta:

        unique_together = (
            "student",
            "subject",
            "attendance_date",
        )

    def __str__(self):
        return f"{self.student} - {self.attendance_date}"


class Exam(TimeStampModel):

    EXAM_TYPES = (
        ("First Terminal", "First Terminal"),
        ("Second Terminal", "Second Terminal"),
        ("Final", "Final"),
        ("Practical", "Practical"),
    )

    exam_name = models.CharField(max_length=100)
    exam_type = models.CharField(max_length=30, choices=EXAM_TYPES)
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    classroom = models.ForeignKey(ClassRoom, on_delete=models.CASCADE)
    start_date = models.DateField()
    end_date = models.DateField()

    def __str__(self):

        return self.exam_name

class Mark(TimeStampModel):

    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name="marks")
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE, related_name="marks")
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name="marks")
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE, related_name="marks")
    full_marks = models.PositiveIntegerField(default=100)
    pass_marks = models.PositiveIntegerField(default=40)
    obtained_marks = models.DecimalField(max_digits=5, decimal_places=2)
    remarks = models.CharField(max_length=200, blank=True)

    class Meta:
        unique_together = (
            "student",
            "subject",
            "exam",
        )

    @property
    def percentage(self):
        return round(
            (self.obtained_marks / self.full_marks) * 100,
            2,
        )

    @property
    def result(self):

        if self.obtained_marks >= self.pass_marks:
            return "Pass"
        return "Fail"

    def __str__(self):
        return f"{self.student} - {self.subject}"