# from django.db import models

# # Create your models here.
# class TimeStampModel(models.Model):
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)

#     class Meta:
#         abstract = True

# class Subject(TimeStampModel):
#     sub_name = models.CharField(max_length=255, null=False, blank=False)
#     course_code = models.CharField(max_length=10, null=False, blank=False)

#     def __str__(self):
#         return self.sub_name

# class UserProfile(TimeStampModel):
#     EXPERIENCE_CHOICES = [
#         ("0-1 year", "0-1 Year"),
#         ("1-2 years", "1-2 Years"),
#         ("above 2 years", "Above 2 Years"),
#     ]
#     teacher_name = models.CharField(max_length=255, null=False, blank=False)
#     image = models.ImageField(upload_to="Teacher/teacher_images/%Y/%m/%d", blank=False)
#     email = models.EmailField(unique=True)
#     address = models.CharField(max_length=255, blank=False)
#     mobile_no = models.IntegerField()
#     subject = models.ManyToManyField(Subject)
#     qualification = models.TextField(blank=False)
#     experience = models.CharField(max_length=13, choices=EXPERIENCE_CHOICES, default="0-1 year")

#     def __str__(self):
#         return self.teacher_name

# class Post(TimeStampModel):
#     title = models.CharField(max_length=255, blank=False)
#     desc = models.TextField(blank=False)
#     teacher = models.ForeignKey("UserProfile", on_delete=models.CASCADE, null=False, blank=False)
    
#     def __str__(self):
#         return self.title


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


class UserProfile(TimeStampModel):
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
    teacher = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name="posts")
    title = models.CharField(max_length=255)
    desc = models.TextField()
    def __str__(self):
        return self.title