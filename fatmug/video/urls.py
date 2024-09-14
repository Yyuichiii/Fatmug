from django.urls import path
from video import views

urlpatterns = [
    path('', views.index,name="index"),
    path('upload', views.upload_video,name="upload_video"),        
    path('list_videos', views.list_videos,name="list_videos"),        
    path('search', views.search,name="search"),        
    path('play_video/<int:id>', views.play_video,name="play_video"),     
    path('subtitle/<int:file_id>/', views.serve_subtitle, name='serve_subtitle'),   
    path('video/serve/<int:id>/', views.serve_video, name='serve_video'),
]