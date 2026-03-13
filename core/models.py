from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class GradeClass(models.Model):
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=20)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name


class Batch(models.Model):
    grade_class = models.ForeignKey(GradeClass, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=20)
    faculty_incharge = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} ({self.grade_class.name})"
    
class LiveSession(models.Model):

    enquiry_id = models.IntegerField()

    meeting_link = models.URLField()

    session_date = models.DateField()
    session_time = models.TimeField()

    created_at = models.DateTimeField(auto_now_add=True)