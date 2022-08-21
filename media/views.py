from django.shortcuts import get_object_or_404, render
from .models import Video, Gallery, VIDEO_CATEGORIES, GALLERY_CATEGORIES
# Create your views here.


def galleryStapel(request):
    galleries = Gallery.objects.all()
    context = {
        'galleries': galleries
    }
    return render(request, 'media/gallery-stapel.html', context)


def videoMasonary(request):
    videos = Video.objects.all()
    context = {
        'video_galleries': videos,
        'video_categories': VIDEO_CATEGORIES
    }
    return render(request, 'media/video-masonary.html', context)


def galleryMasonary(request):
    galleries = Gallery.objects.all()

    context = {
        'galleries': galleries,
        'gallery_categories': GALLERY_CATEGORIES
    }
    return render(request, 'media/gallery-masonary.html', context)


def videoByCategory(request, category):
    videos = Video.objects.all().filter(category=category[0])
    context = {
        'videos': videos,
        'category': category
    }
    return render(request, 'media/video-category.html', context)


def videoDetail(request, pk):
    video = get_object_or_404(Video, pk=pk)
    context = {
        'video': video
    }
    return render(request, 'media/video-detail.html', context)


def galleryDetail(request, pk):
    gallery = get_object_or_404(Gallery, pk=pk)
    context = {
        'gallery': gallery
    }
    return render(request, 'media/gallery-full-view.html', context)


def galleryByCategory(request, category):
    galleries = Gallery.objects.all().filter(category=category)
    context = {
        'galleries': galleries
    }
    return render(request, 'media/video-category.html', context)
