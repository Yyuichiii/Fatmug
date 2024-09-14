from celery import shared_task
from .models import StatusChoice,UploadedVideo,Subtitle,SubtitleFile
import subprocess
import re
from django.utils.dateparse import parse_duration
from django.conf import settings
import os
from pathlib import Path
from langdetect import detect, LangDetectException
from .language import LANGUAGE_CODE_TO_NAME
from django.core.files import File
from django.core.files.base import ContentFile

@shared_task
def video_extraction_process(pk):
    # Get the uploaded video object
    upload = UploadedVideo.objects.get(pk=pk)

    # Path to the video file
    video_path = upload.video.path

    # Path to the subtitles output folder
    output_folder = os.path.join(settings.MEDIA_ROOT, 'temp')
    os.makedirs(output_folder, exist_ok=True)

    # FFprobe command to get subtitle stream indexes
    command = [
        'ffprobe', '-v', 'error', '-select_streams', 's', 
        '-show_entries', 'stream=index', '-of', 'csv=p=0', video_path
    ]
    
    # Run the ffprobe command and capture the output
    result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    
    # Parse the subtitle streams
    subtitle_streams = result.stdout.strip().split('\n')



    if not subtitle_streams or all(item == '' for item in subtitle_streams):
        upload.status = StatusChoice.COMPLETED
        upload.save()
        return


    # Get the file name without the extension
    video_name_without_extension = os.path.splitext(os.path.basename(upload.video.name))[0]

    # Loop through each subtitle stream and extract it using ffmpeg
    for stream in subtitle_streams:
        # Output file path inside the subtitles folder
        output_file = os.path.join(output_folder, f'{video_name_without_extension}_{stream}.vtt')
        
        # Construct the ffmpeg command to extract the subtitle stream
        ffmpeg_command = [
            'ffmpeg', '-i', video_path, '-map', f'0:{stream}','-f', 'webvtt', output_file
        ]
        
        # Run the ffmpeg command
        subprocess.run(ffmpeg_command)


        #Open temporary stored vtt file
        with open(output_file, 'r', encoding='utf-8') as file:
            vtt = file.read()

        try:
            lang_code = LANGUAGE_CODE_TO_NAME.get(detect(vtt),"Unknown")
        except LangDetectException:
            lang_code = "Unknown"
        
        #Contruct new name for the vtt file 
        new_file_name = f"{video_name_without_extension}_{lang_code}.vtt"

        new_file_content = ContentFile(vtt, name=new_file_name)

        SubtitleFile.objects.create(
            video=upload,
            file=new_file_content,
            language=lang_code  
            )

        entries = []
        pattern = re.compile(
    r'(\d{2}:\d{2}\.\d{3}) --> (\d{2}:\d{2}\.\d{3})\n(.+?)(?=\n\d{2}:\d{2}\.\d{3} --> \d{2}:\d{2}\.\d{3}|\Z)',
    re.DOTALL
        )

        for match in pattern.finditer(vtt):
            start, end, text = match.groups()
            language = lang_code
            start_time = parse_duration(start)
            end_time = parse_duration(end)
            entries.append((start_time, end_time, text.replace('\n', ' '),language))

        if os.path.exists(output_file):
            os.remove(output_file)

        srt_content = entries

        subtitle_objects = [
        Subtitle(
                video=upload,
                start_time=start_time,
                end_time=end_time,
                text=text,
                language=language
        )
        for start_time, end_time, text, language in srt_content
        ]

        # Add subtitles text in the model for easy searching
        Subtitle.objects.bulk_create(subtitle_objects)


    
    # Update the upload status to COMPLETED
    upload.status = StatusChoice.COMPLETED
    upload.save()

    return 