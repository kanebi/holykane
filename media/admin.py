from django.contrib import admin
from .models import Video, Gallery, ImageStack

admin.site.register([Video, Gallery, ImageStack])
# Register your models here.
