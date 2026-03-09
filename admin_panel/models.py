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

    categories = models.JSONField()   # multi select store

    sender = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "admin_announcement"

    def __str__(self):
        return self.title



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