from django.urls import path
from video import views

urlpatterns = [
    path('', views.index,name="index"),
    path('upload', views.upload_video,name="upload_video"),        
    path('list_videos', views.list_videos,name="list_videos"),        
    path('search', views.search,name="search"),        
]
