from django.db import models
from django.contrib.auth.models import User


class TimeStampModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Subject(TimeStampModel):
    sub_name = models.CharField(max_length=255)
    course_code = models.CharField(max_length=20, unique=True)

    def __str__(self):
        return self.sub_name


class Teacher(TimeStampModel):
    EXPERIENCE_CHOICES = [
        ("0-1 year", "0-1 Year"),
        ("1-2 years", "1-2 Years"),
        ("above 2 years", "Above 2 Years"),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    image = models.ImageField(upload_to="Teacher/profile/%Y/%m/%d/")
    phone = models.CharField(max_length=15)
    address = models.CharField(max_length=255, blank=False)
    bio = models.TextField(blank=False)
    qualification = models.TextField()
    experience = models.CharField(max_length=15, choices=EXPERIENCE_CHOICES, default="0-1 year")
    subjects = models.ManyToManyField(Subject,related_name="teachers")

    def __str__(self):
        return self.user.get_full_name() or self.user.username


class Post(TimeStampModel):
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE, related_name="posts")
    title = models.CharField(max_length=255)
    desc = models.TextField()
    def __str__(self):
        return self.title