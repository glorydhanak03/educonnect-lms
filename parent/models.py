from django.db import models
from django.conf import settings
from django.core.validators import MinValueValidator, MaxValueValidator


class ParentEnquiry(models.Model):

    SEND_TO_CHOICES = (
        ('admin', 'Admin'),
        ('faculty', 'Faculty'),
    )

    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('in_progress', 'In Progress'),
        ('resolved', 'Resolved'),
    )

    ENQUIRY_TYPE_CHOICES = (
        ('technical', 'Technical Issue'),
        ('academic', 'Academic Related'),
        ('fees', 'Fees Related'),
        ('general', 'General Query'),
    )

    parent = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="parent_enquiries"
    )

    parent_name = models.CharField(max_length=100)
    child_name = models.CharField(max_length=100)
    child_class = models.CharField(max_length=50)

    send_to = models.CharField(max_length=20, choices=SEND_TO_CHOICES)
    receiver_name = models.CharField(max_length=100, blank=True, null=True)

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
        db_table = "parent_enquiry"
        ordering = ['-created_at']

    def __str__(self):
        return f"Parent Enquiry #{self.id} - {self.parent_name}"


class ParentFeedback(models.Model):

    enquiry = models.OneToOneField(
        ParentEnquiry,
        on_delete=models.CASCADE,
        related_name="parent_feedback"
    )

    rating = models.PositiveIntegerField(
        null=True,
        blank=True,
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )

    comment = models.TextField()

    attachment = models.FileField(
        upload_to="parent_feedback_files/",
        null=True,
        blank=True
    )

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "parent_feedback"
        ordering = ['-created_at']

    def __str__(self):
        return f"Parent Feedback #{self.enquiry.id}"
