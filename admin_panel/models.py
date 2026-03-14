from django.db import models
from django.conf import settings


class AdminAnnouncement(models.Model):

    CATEGORY_CHOICES = [
        ('Students','Students'),
        ('Faculty','Faculty'),
        ('Parents','Parents'),
    ]

    title = models.CharField(max_length=200)
    message = models.TextField()

    categories = models.JSONField()   

    sender = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "admin_announcement"

    def __str__(self):
        return self.title

class EnquiryAction(models.Model):

    STATUS_CHOICES = (
        ("approved","Approved"),
        ("rejected","Rejected"),
        ("rescheduled","Rescheduled"),
        ("completed","Completed"),
        ("cancelled","Cancelled"),
    )

    enquiry_id = models.IntegerField()
    enquiry_type = models.CharField(max_length=20)
    action = models.CharField(max_length=20,choices=STATUS_CHOICES)

    reason = models.TextField(blank=True,null=True)

    session_date = models.DateField(blank=True,null=True)
    session_time = models.TimeField(blank=True,null=True)
    meeting_link = models.URLField(blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)


class AdminGuideline(models.Model):

    ROLE_CHOICES = (
        ("student","Student"),
        ("parent","Parent"),
        ("faculty","Faculty"),
    )

    role = models.CharField(max_length=20, choices=ROLE_CHOICES)
    message = models.TextField()

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.role} - Guideline"