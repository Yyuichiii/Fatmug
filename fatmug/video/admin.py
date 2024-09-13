from django.contrib import admin
from .models import UploadedVideo,Subtitle,SubtitleFile

@admin.register(UploadedVideo)
class UploadedVideoAdmin(admin.ModelAdmin):
    list_display = ('video', 'uploaded_at', 'status')
    list_filter = ('status',)
    search_fields = ('video',)
    ordering = ('-uploaded_at',)


@admin.register(Subtitle)
class SubtitleAdmin(admin.ModelAdmin):
    list_display = ('video', 'start_time', 'end_time','text','language')
    list_filter = ('language',)
    search_fields = ('text',)


@admin.register(SubtitleFile)
class SubtitleFileAdmin(admin.ModelAdmin):
    list_display = ('video', 'file','language')
    list_filter = ('language',)
    search_fields = ('language',)
