from django.db import models
from ckeditor_uploader.fields import RichTextUploadingField
from django.urls import reverse
from django.utils import timezone
# Create your models here.

EVENT_CATEGORIES = (
    ('SH', 'Show'),
    ('L', 'Live'),
    ('S', 'Streaming'))


class Event (models.Model):

    title = models.CharField(max_length=200)
    venue = models.CharField(max_length=222)
    date_time = models.DateTimeField()
    location = models.CharField(max_length=255)
    link = models.URLField()
    map_longitude = models.CharField(max_length=200, default=0)
    map_latitude = models.CharField(max_length=200, default=0)
    category = models.CharField(max_length=2, choices=EVENT_CATEGORIES)
    cover = models.ImageField(upload_to='events/images/')

    content = RichTextUploadingField(config_name='awesome_ckeditor')

    created_on = models.DateTimeField(auto_now_add=True)  # Date of creation
    updated_on = models.DateTimeField(auto_now=True)  # Date of updation

    def timeLeft(self):
        diff = self.date_time - timezone.now()
        return {'days': diff.days, 'hour': round(diff.total_seconds() / (60*60)), 'minutes': round(diff.total_seconds() / 60)}

    def get_absolute_url(self):
        return reverse('events:detail', kwargs={'pk': self.pk})

    def get_category_url(self):
        return reverse('events:category', kwargs={'category': self.get_category_display()})
