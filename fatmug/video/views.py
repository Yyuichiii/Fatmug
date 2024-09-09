from django.shortcuts import render,redirect
from django.http import HttpResponse
from .models import UploadedVideo
from django.contrib import messages
# Create your views here.

def index(request):
    return render(request,"video/index.html")


def upload_video(request):

    if request.method =="POST":
        video_file = request.FILES.get('video')
        if video_file:
            # Save the uploaded video
            UploadedVideo.objects.create(video=video_file)    
            videos = UploadedVideo.objects.all 
            messages.success(request, 'Your video has been uploaded successfully!')
            return redirect('list_videos',context={"videos":videos})
    return render(request,"video/upload.html")


def list_videos(request):
    videos = UploadedVideo.objects.all
    return render(request,"video/list.html",context={"videos":videos})


def search(request):
    return render(request,"video/search.html")
