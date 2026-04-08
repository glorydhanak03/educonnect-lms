#from django.db import models

# Create your models here.
from django.contrib.auth.models import AbstractUser
from django.db import models



class User(AbstractUser):
    ROLE_CHOICES = (
        ("STUDENT", "Student"),
        ("FACULTY", "Faculty"),
        ("PARENT", "Parent"),
    )

    role = models.CharField(max_length=20, choices=ROLE_CHOICES)
    mobile = models.CharField(max_length=15)

    class_name = models.CharField(max_length=50, blank=True, null=True)
    section = models.CharField(max_length=10, blank=True, null=True)
