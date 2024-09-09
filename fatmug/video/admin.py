from django.contrib import admin
from .models import UploadedVideo

@admin.register(UploadedVideo)
class UploadedVideoAdmin(admin.ModelAdmin):
    list_display = ('video', 'uploaded_at', 'status')
    list_filter = ('status',)
    search_fields = ('video',)
    ordering = ('-uploaded_at',)