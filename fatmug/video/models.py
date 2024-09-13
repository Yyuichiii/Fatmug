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
    



class Subtitle(models.Model):
    video = models.ForeignKey('UploadedVideo', on_delete=models.CASCADE) 
    start_time = models.DurationField()
    end_time = models.DurationField()
    text = models.TextField()
    language = models.CharField(max_length=20, blank=True, null=True)

    class Meta:
        indexes = [
            models.Index(fields=['video', 'start_time']),
        ]

class SubtitleFile(models.Model):
    video = models.ForeignKey('UploadedVideo', on_delete=models.CASCADE)
    file = models.FileField(upload_to='videos/subtitles/')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    language = models.CharField(max_length=20, blank=True, null=True)

    def __str__(self):
        return f"{self.file.name} ({self.language})"
    