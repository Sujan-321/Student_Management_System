from django.db import models
from django.conf import settings

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


    def __str__(self):
        return f"{self.first_name} {self.last_name}"

