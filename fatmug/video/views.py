from django.shortcuts import render,redirect
from django.http import HttpResponse
from .models import UploadedVideo
from .tasks import video_extraction_process
from django.contrib import messages


def index(request):
    return render(request,"video/index.html")


def upload_video(request):

    if request.method =="POST":
        
        video_file = request.FILES.get('video')
        if video_file:
            # Save the uploaded video
            upload = UploadedVideo.objects.create(video=video_file)    
            video_extraction_process.delay_on_commit(upload.pk)
            messages.success(request, 'Your video has been uploaded successfully!')
            return redirect('list_videos')
    return render(request,"video/upload.html")


def list_videos(request):
    videos = UploadedVideo.objects.all().order_by('-uploaded_at')
    return render(request,"video/list.html",context={"videos":videos})


def search(request):
    return render(request,"video/search.html")
