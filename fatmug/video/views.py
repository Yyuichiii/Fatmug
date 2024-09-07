from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.

def index(request):
    return render(request,"video/index.html")


def upload_video(request):
    return render(request,"video/upload.html")


def list_videos(request):
    return render(request,"video/list.html")


def search(request):
    return render(request,"video/search.html")
