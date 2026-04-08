from symtable import Class

from django.db import models
from accounts.models import User


class Assignment(models.Model):

    title = models.CharField(max_length=200)

    description = models.TextField()

    subject = models.CharField(max_length=200)

    class_name = models.CharField(max_length=50)
    
    section = models.CharField(max_length=10)

    faculty = models.ForeignKey(
    User,
    on_delete=models.CASCADE,
    related_name="teacher_assignments"
    
)

    start_date = models.DateField()

    due_date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)

    total_marks = models.IntegerField()

    question_file = models.FileField(
        upload_to="assignments/questions/",
        blank=True,
        null=True
    )

    

    def __str__(self):
        return self.title


class AssignmentQuestion(models.Model):

    assignment = models.ForeignKey(
        Assignment,
        on_delete=models.CASCADE,
        related_name="questions"
    )

    question_text = models.TextField()

    question_type = models.CharField(
        max_length=50,
        choices=[
            ("short", "Short Notes"),
            ("long", "Long Answer"),
            ("mcq", "MCQ"),
        ]
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.question_text
