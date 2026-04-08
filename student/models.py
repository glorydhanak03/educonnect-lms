from django.db import models
from accounts.models import User
from faculty.models import Assignment

class AssignmentSubmission(models.Model):

    assignment = models.ForeignKey(
        Assignment,
        on_delete=models.CASCADE,
        related_name="submissions"
    )

    student = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )

    file = models.FileField(upload_to="assignments/submissions/")
    answers = models.TextField(blank=True, null=True)

    submitted_at = models.DateTimeField(auto_now_add=True)

    status = models.CharField(
        max_length=20,
        choices=[
            ('submitted', 'Submitted'),
            ('graded', 'Graded')
        ],
        default='submitted'
    )

    marks = models.IntegerField(null=True, blank=True)

    feedback = models.TextField(blank=True)

    class Meta:
        unique_together = ['assignment', 'student']
    
    def __str__(self):
        return f"{self.student} - {self.assignment}"