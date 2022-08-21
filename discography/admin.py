from django.contrib import admin
from .models import Song,  Genre, Stream, Download
# Register your models here.
admin.site.register([

    Song,  Genre, Stream, Download

])
