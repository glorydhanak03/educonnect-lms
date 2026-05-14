from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    ROLE_CHOICES = (
        ('student','Student'),
        ('faculty','Faculty'),
        ('parent','Parent'),
        ('admin','Admin'),
    )
    contact_number = models.CharField(max_length=15)
    mobile = models.CharField(max_length=15, null=True, blank=True)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES)


  

    class_name = models.CharField(max_length=50, blank=True, null=True)
    section = models.CharField(max_length=10, blank=True, null=True)


class StudentProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    grade_class = models.ForeignKey("core.GradeClass", on_delete=models.CASCADE)
    batch = models.ForeignKey("core.Batch", on_delete=models.SET_NULL, null=True, blank=True)
    roll_number = models.CharField(max_length=50, blank=True)
    admission_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return self.user.username


class ParentProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    linked_student = models.ForeignKey("accounts.StudentProfile", on_delete=models.SET_NULL, null=True)
    relation_type = models.CharField(max_length=50)
    alternate_contact = models.CharField(max_length=15, blank=True)

    def __str__(self):
        return self.user.username


class FacultyProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    department = models.CharField(max_length=100, blank=True)
    assigned_grade_class = models.ForeignKey("core.GradeClass", on_delete=models.SET_NULL, null=True, blank=True)
    assigned_batch = models.ForeignKey("core.Batch", on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.user.username
