import json
from django.conf import settings
from django.db import models
from djmoney import money
# Create your models here.
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils.text import slugify
from taggit.managers import TaggableManager
from ckeditor_uploader.fields import RichTextUploadingField
from django.apps import apps

ALBUM_CATEGORIES = (('A', 'ALBUMS'), ('S', 'SINGLE'),
                    ('E', 'Extended-Play'))


class Stream(models.Model):

    song = models.ForeignKey(
        'Song', related_name='streams', on_delete=models.CASCADE)
    sessionID = models.CharField(
        max_length=200,  null=True, blank=True)
    user = models.ForeignKey(User,
                             on_delete=models.CASCADE)
    created_on = models.DateTimeField(auto_now_add=True)  # Date of creation
    updated_on = models.DateTimeField(auto_now=True)  # Date of updation
    count = models.IntegerField(default=0)


class Download(models.Model):
    count = models.IntegerField(default=0)

    song = models.ForeignKey(
        'Song', related_name='downloads', on_delete=models.CASCADE)
    sessionID = models.CharField(
        max_length=200,  null=True, blank=True)
    user = models.ForeignKey(User,
                             on_delete=models.CASCADE)
    created_on = models.DateTimeField(auto_now_add=True)  # Date of creation
    updated_on = models.DateTimeField(auto_now=True)  # Date of updation


class Song(models.Model):
    artist = models.CharField(max_length=200, default='Holykane')
    title = models.CharField(max_length=255)
    sku = models.CharField(max_length=222, blank=True, null=True)
    upc = models.CharField(max_length=222, blank=True, null=True)
    created_on = models.DateTimeField(auto_now_add=True)  # Date of creation
    updated_on = models.DateTimeField(auto_now=True)  # Date of updation
    lyrics = models.TextField(max_length=1000, blank=True, null=True)
    producers = TaggableManager(blank=True, help_text='Producers')
    audio = models.FileField(upload_to='songs/audios')
    downloadable = models.BooleanField(default=False)
    version = models.CharField(max_length=200, null=True, blank=True)
    genre = models.ForeignKey(
        'Genre', related_name='genre_songs', on_delete=models.CASCADE)
    embed_frame = models.TextField(max_length=6000, null=True, blank=True)

    def get_total_streams(self):
        return sum([item.count for item in self.streams.all()])

    def get_serialized(self):
        dict_s = {'title': self.title, 'cover': self.album.all(
        )[0].cover.url, 'artist': self.artist, 'pk': self.pk, 'audio': self.audio.url, }
        return json.dumps(dict_s)

    def get_update_downloads_url(self):
        return reverse('discography:update-downloads', kwargs={'pk': self.pk})

    def get_update_streams_url(self):
        return reverse('discography:update-streams', kwargs={'pk': self.pk})

    def get_remove_from_wish_url(self):
        return reverse('discography:remove-from-wish', kwargs={'pk': self.pk, 'type': 'song'})

    def __str__(self):
        return self.title

    # def get_absolute_url(self):
    #     return reverse("discography:song", kwargs={'slug': self.slug})


class Genre(models.Model):
    name = models.CharField(max_length=100)
    content = RichTextUploadingField(config_name='awesome_ckeditor')
    cover = models.ImageField(upload_to='genre/images/')

    created_on = models.DateTimeField(auto_now_add=True)  # Date of creation
    updated_on = models.DateTimeField(auto_now=True)  # Date of updation

    def __str__(self):
        return self.name
