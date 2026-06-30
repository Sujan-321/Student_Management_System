# from django.db import models

# # Create your models here.
# class TimeStampModel(models.Model):
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)

#     class Meta:
#         abstract = True

# class Subject(models.Model):
#     sub_name = models.CharField(max_length=255, null=False, blank=False)
#     course_code = models.CharField(max_length=10, null=False, blank=False)

#     def __str__(self):
#         return self.sub_name

# class UserProfile(models.Model):
#     EXPERIENCE_CHOICES = [
#         ("0-1 year", "0-1 Year"),
#         ("1-2 year", "1-2 Years"),
#         ("above 2 year", "Above 2 Years"),
#     ]
#     teacher_name = models.CharField(max_length=255, null=False, blank=False)
#     email = models.EmailField(unique=True)
#     address = models.CharField(max_length=255, blank=False)
#     mobile_no = models.IntegerField(max_length=10)
#     subject = models.ManyToManyField(Subject)
#     qualification = models.TextField(blank=False)
#     experience = models.CharField(max_length=13, choices=EXPERIENCE_CHOICES, default="0-1 year")

#     def __str__(self):
#         return self.teacher_name

# class Post(models.Model):
#     title = models.CharField(max_length=255, blank=False)
#     desc = models.TextField()
