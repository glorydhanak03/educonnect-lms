from django.db import models
from django.conf import settings  

class FacultyAnnouncement(models.Model):
    POST_TO_CHOICES = [
        ('Students', 'Students'),
        ('Parents', 'Parents'),
        ('Both', 'Both'),
    ]

    faculty = models.ForeignKey(
        settings.AUTH_USER_MODEL,  
        on_delete=models.CASCADE
    )
    title = models.CharField(max_length=200)
    announcement = models.TextField()
    std_class = models.CharField(max_length=50,blank=True)
    subject = models.CharField(max_length=50,blank=True)
    post_to = models.CharField(max_length=20, choices=POST_TO_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "faculty_announcement"  

    def __str__(self):
        return f"{self.title} - {self.faculty}"