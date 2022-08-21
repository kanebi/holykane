from django.contrib import admin
from .models import BlogPost, Comment, Category


admin.site.register([BlogPost, Comment, Category])
# Register your models here.
