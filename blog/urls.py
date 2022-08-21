
from django.contrib import admin
from django.urls import path, include
from .views import blogDetail, byCategory, add_comment, index

app_name = 'blog'
urlpatterns = [
    path('<date>/<slug>/', blogDetail, name='blog-detail'),
    path('category/<title>/', byCategory, name='by-category'),
    path('add-comment/<blog_id>',
         add_comment, name='add-comment'),
    path('', index, name='home'),
]
