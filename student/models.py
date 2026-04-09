from django.db import models
<<<<<<< HEAD
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
=======
from django.conf import settings
from django.core.validators import MinValueValidator, MaxValueValidator


class Enquiry(models.Model):

    SEND_TO_CHOICES = (
        ('admin', 'Admin'),
        ('faculty', 'Faculty'),
    )

    STATUS_CHOICES = [
        ("pending","Pending"),
        ("in_progress","In Progress"),
        ("approved","Approved"),
        ("completed","Completed"),
        ("closed","Closed"),
    ]
    
    ENQUIRY_TYPE_CHOICES = (
        ('technical', 'Technical Issue'),
        ('course', 'Course Related'),
        ('payment', 'Payment Issue'),
        ('general', 'General Query'),
    )

    student = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="enquiries"
    )

    student_name = models.CharField(max_length=100)
    student_class = models.CharField(max_length=50)

    send_to = models.CharField(max_length=20, choices=SEND_TO_CHOICES)
    receiver_name = models.CharField(max_length=100, blank=True, null=True)

    course_name = models.CharField(max_length=100, default="Not Specified")

    enquiry_type = models.CharField(
        max_length=50,
        choices=ENQUIRY_TYPE_CHOICES
    )

    date = models.DateField()
    time_slot = models.TimeField()
    message = models.TextField()

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="pending"
    )

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Enquiry #{self.id} - {self.student_name} ({self.status})"


class Feedback(models.Model):

    enquiry = models.OneToOneField(
        Enquiry,
        on_delete=models.CASCADE,
        related_name="feedback"
    )

    rating = models.PositiveIntegerField(
    null=True,
    blank=True,
    validators=[MinValueValidator(1), MaxValueValidator(5)]
    )
    comment = models.TextField()
    attachment = models.FileField(
        upload_to="feedback_files/",
        null=True,
        blank=True
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Feedback for Enquiry #{self.enquiry.id}"
    
    @property
    def formatted_id(self):
        return f"SENQ-{self.id}"
>>>>>>> main
