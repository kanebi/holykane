from unicodedata import category
from django.db import models
from ckeditor_uploader.fields import RichTextUploadingField
from django.urls import reverse
# Create your models here.
GALLERY_CATEGORIES = (
    ('T', 'Tour'),
    ('S', 'Scene-Shots'),
    ('L', 'Live'),
    ('C', 'Concerts'),

)


class ImageStack(models.Model):
    image = models.ImageField(upload_to='gallery/images')
    title = models.CharField(max_length=200)
    location = models.CharField(max_length=200)
    created_on = models.DateTimeField(auto_now_add=True)  # Date of creation
    updated_on = models.DateTimeField(auto_now=True)  # Date of updation


class Gallery (models.Model):
    title = models.CharField(max_length=200)
    images = models.ManyToManyField(ImageStack, related_name='root_src')
    mainCover = models.ImageField(upload_to='gallery-main-cover/images')
    created_on = models.DateTimeField(auto_now_add=True)  # Date of creation
    updated_on = models.DateTimeField(auto_now=True)  # Date of updation
    description = RichTextUploadingField(
        config_name='awesome_ckeditor', null=True, blank=True)
    category = models.CharField(max_length=10, choices=GALLERY_CATEGORIES)

    def get_cover_url(self):
        if self.mainCover:
            return self.mainCover.url
        cover_url = self.images.all()[0].image.url
        return cover_url

    def get_absolute_url(self):
        return reverse('media:gallery-detail', kwargs={'pk': self.pk})

    def get_category_url(self):
        return reverse('media:gallery-category', kwargs={'category': self.get_category_display()})


VIDEO_CATEGORIES = (
    # ('OMV', 'Official Music Video'),
    ('L', 'Live'),
    ('G', 'Guests'),
    # ('UMV', 'UnOfficial Music Video'),
    ('P', 'PARTIES'),
    ('S', 'SHOWS'),

)


class Video(models.Model):
    title = models.CharField(max_length=200)
    video = models.FileField(upload_to='videos')
    link = models.URLField()
    cover = models.ImageField(upload_to='gallery/images')

    location = models.CharField(max_length=200)
    date = models.DateTimeField(auto_now_add=True)  # Date of creation
    created_on = models.DateTimeField(auto_now_add=True)  # Date of creation
    updated_on = models.DateTimeField(auto_now=True)  # Date of updation
    description = RichTextUploadingField(
        config_name='awesome_ckeditor', null=True, blank=True)
    category = models.CharField(max_length=10, choices=VIDEO_CATEGORIES)

    def get_absolute_url(self):
        return reverse('media:video-detail', kwargs={'pk': self.pk})

    def get_category_url(self):
        return reverse('media:video-category', kwargs={'category': self.get_category_display()})
