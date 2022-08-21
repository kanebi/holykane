from django.conf import settings
from django.db import models
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.contrib.auth.models import User
from phonenumber_field.modelfields import PhoneNumberField
from django_countries.fields import CountryField
from ckeditor_uploader.fields import RichTextUploadingField
from discography.models import Song
from djmoney import money
SHIPPING_FEE = money.Money(0.4, 'USD')


class Slides (models.Model):
    name_id = models.CharField(max_length=100)
    action_text = models.CharField(max_length=100)
    title = models.CharField(max_length=100)
    sub_title = models.CharField(max_length=100)
    image = models.ImageField(upload_to='homepage/slides')
    location_url = models.URLField()
    description = RichTextUploadingField(
        blank=True, null=True,
        config_name='awesome_ckeditor')


class AboutPage(models.Model):
    name_id = models.CharField(max_length=100)

    title = models.CharField(max_length=100)
    description = RichTextUploadingField(
        blank=True, null=True,
        config_name='awesome_ckeditor')


class Header(models.Model):
    name_id = models.CharField(max_length=100)

    logo = models.ImageField(upload_to='header/logo')


class HomePage(models.Model):

    name_id = models.CharField(max_length=100)
    about_artist = RichTextUploadingField(
        config_name='awesome_ckeditor', null=True)
    about_artist_bg = models.ImageField(
        upload_to='homepage/aboutBg', null=True)

    slides = models.ManyToManyField(Slides, related_name='homepage')
    recommended_tracks = models.ManyToManyField(
        Song, related_name='recommendation')


class ContactPage(models.Model):
    name_id = models.CharField(max_length=100)
    page_title = models.CharField(max_length=100)
    intro_text = RichTextUploadingField(config_name='awesome_ckeditor')


class UserProfile(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name='profile')
    picture = models.ImageField(upload_to='user/image', blank=True, null=True)
    phone = PhoneNumberField(blank=True, null=True)
    country = CountryField(blank=True, null=True)

    def get_cart_sub_total(self):
        cart = self.user.carts.all().filter(ordered=False)
        sum_total = sum([item.get_final_sum_price() for item in cart])
        return sum_total

    def get_cart_total(self):
        total = self.get_cart_sub_total() + SHIPPING_FEE
        return total


class ContactUs(models.Model):
    sender_name = models.CharField(max_length=222)
    email = models.EmailField()
    subject = models.CharField(max_length=200)
    message = models.TextField(max_length=10000)

    created_on = models.DateTimeField(auto_now_add=True)  # Date of creation
    updated_on = models.DateTimeField(auto_now=True)  # Date of updation


class Newsletter(models.Model):
    email = models.EmailField()

    subscribed = models.BooleanField(default=True)
    created_on = models.DateTimeField(auto_now_add=True)  # Date of creation
    updated_on = models.DateTimeField(auto_now=True)  # Date of updation


# UserProfile receiver


def userprofile_receiver(sender, instance, created, *args, **kwargs):
    if created:
        userprofile = UserProfile.objects.create(user=instance)


post_save.connect(userprofile_receiver, sender=User)
