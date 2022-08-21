
from django.contrib import admin
from django.urls import path, include
from .views import videoByCategory, videoDetail, galleryDetail, galleryByCategory, galleryMasonary, galleryStapel, videoMasonary
app_name = 'media'
urlpatterns = [

    path('video/category/<category>', videoByCategory, name='video-category'),
    path('video/detail/<pk>', videoDetail, name='video-detail'),
    path('gallery/category/<category>',
         galleryByCategory, name='gallery-category'),
    path('gallery/detail/<pk>', galleryDetail, name='gallery-detail'),
    path('video/masonary/', videoMasonary, name='video-masonry'),
    path('', galleryMasonary, name='gallery-masonry'),
    path('gallery/stapel/', galleryStapel, name='gallery-stapel'),
]
