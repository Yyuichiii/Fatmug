from django.shortcuts import render,redirect
from django.http import HttpResponse,FileResponse
from .models import UploadedVideo,SubtitleFile
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


def play_video(request, id):
    video = UploadedVideo.objects.get(pk=id)
    subtitles = SubtitleFile.objects.filter(video=video)
    

    subtitle_files = {
        subtitle.language: subtitle.file.path
        for subtitle in subtitles
    }

    context = {
        "video": video,
        "subtitles": subtitles,
        "subtitle_files": subtitle_files,
    }

    return render(request, "video/video_play.html", context)

def serve_subtitle(request, file_id):
    subtitle = SubtitleFile.objects.get(pk=file_id)
    file_path = subtitle.file.path
    response = FileResponse(open(file_path, 'rb'), content_type='text/vtt')
    response['Content-Disposition'] = f'inline; filename="{subtitle.file.name}"'
    return response