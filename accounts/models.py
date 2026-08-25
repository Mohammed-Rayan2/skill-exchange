from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    student_id = models.CharField(max_length=20,  blank=True, default='')
    course = models.CharField(max_length=100, blank=True, default='')
    auth_type = models.CharField(max_length=10,  default='manual')

    def __str__(self):
        return self.get_full_name() or self.username

    @property
    def display_name(self):
        return self.get_full_name() or self.username

    @property
    def display_course(self):
        val = str(self.course) if self.course else ''
        return val if val.strip() else 'Course not set'
