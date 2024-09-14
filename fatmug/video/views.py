from django.shortcuts import render,redirect
from django.http import FileResponse,JsonResponse
from .models import UploadedVideo,SubtitleFile,Subtitle
from .tasks import video_extraction_process
from django.contrib import messages
from django.urls import reverse
from urllib.parse import urlencode

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



def format_duration(duration):

    total_seconds = int(duration.total_seconds())
    hours, remainder = divmod(total_seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    milliseconds = duration.microseconds / 1000  

    if hours > 0:
        formatted_time = f"{hours}h{minutes}m{seconds}.{int(milliseconds)}s"
    else:
        formatted_time = f"{minutes}m{seconds}.{int(milliseconds)}s"

    return formatted_time

def search(request):

    if request.method == "POST":
        query = request.POST.get('query')
        if query:

            results = Subtitle.objects.filter(text__icontains=query)

            videos = []
            for subtitle in results:
                base_url = reverse('play_video', args=[subtitle.video.pk])
                start_time = format_duration(subtitle.start_time)
                language = subtitle.language
                query_params = {
                    'start_time': start_time,
                    'language': language,
                    }
                full_url = f"{base_url}?{urlencode(query_params)}"
                videos.append({
                    'title': subtitle.video.video.name,
                    'language': language,
                    'start_time': start_time,
                    'text': subtitle.text,
                    'url': full_url
                })

            return JsonResponse({'videos': videos})


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


def serve_video(request, id):
    video = UploadedVideo.objects.get(pk=id)
    response = FileResponse(open(video.video.path, 'rb'), content_type='video/mp4')
    response['Accept-Ranges'] = 'bytes'
    return response






# ffmpeg -i test1.mp4 -c:v libx264 -c:a aac -b:v 1000k -b:a 128k -movflags +faststart -y output-seekable.mp4
# ffprobe output-seekable.mp4
