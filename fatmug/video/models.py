from django.db import models

class StatusChoice(models.TextChoices):
    PENDING = "pending", "Pending"
    COMPLETED = "completed", "Completed"

class UploadedVideo(models.Model):
    video = models.FileField(upload_to='videos/')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(
        max_length=10,
        choices=StatusChoice.choices,
        default=StatusChoice.PENDING
    )

    def __str__(self):
        return f"{self.video.name} ({self.get_status_display()})"