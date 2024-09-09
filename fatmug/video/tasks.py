from celery import shared_task
from .models import StatusChoice,UploadedVideo

@shared_task
def video_extraction_process(pk):
    upload = UploadedVideo.objects.get(pk=pk)
    upload.status=StatusChoice.COMPLETED
    upload.save()
    return 