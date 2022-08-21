import json
import random
import string
from django.conf import settings
from django.db import models
from djmoney import money
# Create your models here.
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils.text import slugify
from taggit.managers import TaggableManager
from ckeditor_uploader.fields import RichTextUploadingField
from django_countries.fields import CountryField
from djmoney.models.fields import MoneyField
from django.db.models.signals import post_save
from django.core import serializers
from discography.models import Song, Genre, ALBUM_CATEGORIES
from core.models import SHIPPING_FEE
from phonenumber_field.modelfields import PhoneNumberField

# Create your models here.


class Favourite(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='favourite_songs')
    album = models.ForeignKey(
        'Album', on_delete=models.CASCADE, related_name='faved')
    songs = models.ManyToManyField(Song, related_name='favs')
    sessionID = models.CharField(
        max_length=200, null=True, blank=True)
    created_on = models.DateTimeField(auto_now_add=True)  # Date of creation
    updated_on = models.DateTimeField(auto_now=True)  # Date of updation


class FileManager(models.Model):
    name = models.CharField(max_length=100, default='')
    description = models.TextField(max_length=5000)
    type = models.CharField(max_length=10, default='I',
                            choices=(('I', 'Images'), ('V', 'Videos'), ('A', 'Audio'), ('G', 'GIF')))
    created_on = models.DateTimeField(auto_now_add=True)  # Date of creation
    updated_on = models.DateTimeField(auto_now=True)  # Date of updation
    file = models.FileField(upload_to='files/')

    def __str__(self):
        return self.name


class Album(models.Model):
    class Meta:
        verbose_name = 'Product'
        verbose_name_plural = 'Products'
    artist = models.ForeignKey(User, on_delete=models.CASCADE)

    title = models.CharField(max_length=255)
    songs = models.ManyToManyField(
        Song, related_name='album')
    release_date = models.DateTimeField()
    cover = models.ImageField(upload_to='album/images/')
    additional_files = models.ManyToManyField(
        FileManager, blank=True, related_name='album_files')
    sku = models.CharField(max_length=222, blank=True, null=True)
    upc = models.CharField(max_length=222, blank=True, null=True)
    price = MoneyField(
        decimal_places=1, default_currency=settings.DEFAULT_MONEY_CURRENCY, max_digits=10)
    discount_price = MoneyField(
        decimal_places=1, default=0.0, default_currency=settings.DEFAULT_MONEY_CURRENCY, max_digits=10)
    record_label = models.CharField(max_length=255)

    shop_link = models.URLField()
    catalog_number = models.CharField(max_length=255, blank=True, null=True)
    slug = models.SlugField(blank=True, null=True)
    description = RichTextUploadingField(config_name='awesome_ckeditor')
    category = models.CharField(max_length=10, choices=ALBUM_CATEGORIES)
    tags = TaggableManager()  # Tags for a Particular Article, You need to install Taggit
    genre = models.ForeignKey(
        Genre, related_name='genre_album', on_delete=models.CASCADE)
    # Keywords to be used in SEO
    keywords = models.CharField(max_length=250, blank=True, null=True)
    created_on = models.DateTimeField(auto_now_add=True)  # Date of creation
    updated_on = models.DateTimeField(auto_now=True)  # Date of updation

    audiomack_link = models.URLField(blank=True, null=True)
    spotify_link = models.URLField(blank=True, null=True)
    itunes_link = models.URLField(blank=True, null=True)
    youtube_link = models.URLField(blank=True, null=True)
    type = models.CharField(max_length=1, choices=(
        ('T', 'Track'), ('M', 'Merch')))

    def __str__(self):
        return self.title

    def get_total_streams(self):

        return sum([sum([item.count for item in song.streams.all()]) for song in self.songs.all()])

    def get_absolute_url(self):
        return reverse("discography:album-detail",  kwargs={'slug': self.slug, 'pk': self.pk})

    def get_category_url(self):
        return reverse("discography:products-by-category",  kwargs={'category': self.get_category_display()})

    def get_shop_url(self):
        return reverse("discography:product-detail", kwargs={'slug': self.slug, 'pk': self.pk})

    def get_add_to_cart_url(self):
        return reverse("discography:add-to-cart", kwargs={'slug': self.slug})

    def get_remove_from_cart_url(self):
        return reverse("discography:remove-from-cart", kwargs={'slug': self.slug})

    def get_add_review_url(self):
        return reverse('discography:add-review', kwargs={'product_id': self.id})

    def get_price(self):
        if self.discount_price.amount >= 1:
            return self.discount_price
        else:
            return self.price

    def is_merch(self):
        if self.category == 'M':
            return True
        else:
            return False

    def is_album(self):
        if self.category == 'A':
            return True
        else:
            return False

    def is_EP(self):
        if self.category == 'E':
            return True
        else:
            return False

    def is_single(self):
        if self.category == 'S':
            return True
        else:
            return False

    def available_discount(self):
        if self.discount_price.amount <= 0 or None:
            return False
        else:
            return True


# Order Item, checks on a particular item if ordered


class Cart(models.Model):
    user = models.ForeignKey(User, null=True,
                             on_delete=models.CASCADE, related_name='carts')
    sessionID = models.CharField(
        max_length=200,  null=True, blank=True)
    ordered = models.BooleanField(default=False)
    item = models.ForeignKey(Album, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)

    def __str__(self):
        return f"{self.quantity} of {self.item.title}"

    def get_total_item_price(self):
        return self.quantity * self.item.price

    def get_total_discount_item_price(self):
        return self.quantity * self.item.discount_price

    def get_amount_saved(self):
        return self.get_total_item_price() - self.get_total_discount_item_price()

    def get_final_sum_price(self):
        if self.item.discount_price.amount >= 1:
            return self.get_total_discount_item_price()
        return self.get_total_item_price()

    def __str__(self):

        if self.user:
            return self.user.username
        if self.sessionID:
            return self.sessionID
        else:
            return f'{self.id}'


# Order Model, Details on the Order made
class Order(models.Model):
    user = models.ForeignKey(User,
                             on_delete=models.CASCADE, blank=True, null=True, related_name='orders')
    ref_code = models.CharField(
        max_length=20, blank=True, unique=True, null=True)
    items = models.ManyToManyField(Cart, related_name='parent_orders')
    start_date = models.DateTimeField(auto_now_add=True)
    ordered_date = models.DateTimeField(blank=True, null=True)
    ordered = models.BooleanField(default=False)
    shipping_address = models.ForeignKey(
        'Address', related_name='shipping_address', on_delete=models.SET_NULL, blank=True, null=True)
    billing_address = models.ForeignKey(
        'Address', related_name='billing_address', on_delete=models.SET_NULL, blank=True, null=True)
    payment = models.ForeignKey(
        'Payment', on_delete=models.SET_NULL, blank=True, null=True)
    coupon = models.ForeignKey(
        'Coupon', on_delete=models.SET_NULL, blank=True, null=True)

    status = models.CharField(max_length=3, default='N', choices=(('N', 'None'),
                                                                  ('P', 'Placed'), ('D', 'Delivered'), ('C', 'Shipped'), ('C', 'Cancelled'))

                              )
    received = models.BooleanField(default=False)
    refund_requested = models.BooleanField(default=False)
    refund_granted = models.BooleanField(default=False)
    sessionID = models.CharField(
        max_length=200,  null=True, blank=True)

    def __str__(self):

        if self.user:
            return self.user.username
        if self.sessionID:
            return self.sessionID
        else:
            return f'{self.id}'

    def get_total(self):
        total = 0
        for order_item in self.items.all():
            total += order_item.get_final_sum_price()
        if self.coupon:
            total -= self.coupon.amount
        return total + SHIPPING_FEE

    def get_subtotal(self):
        sub_total = self.get_total() - SHIPPING_FEE

        return sub_total

    def shipping_fee(self):
        return SHIPPING_FEE

    def get_absolute_url(self):
        return reverse('shop:order-detail', kwargs={'code': self.ref_code})

# Address Model


ADDRESS_CHOICES = (('S', 'Shipping Address'), ('B', 'Billing Address'))


class Address(models.Model):
    user = models.ForeignKey(User,
                             on_delete=models.CASCADE, blank=True, related_name='addresses', null=True)
    state = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    apartment_address = models.CharField(max_length=100)
    country = CountryField(multiple=False)
    zip = models.CharField(max_length=100)
    address_type = models.CharField(max_length=1, choices=ADDRESS_CHOICES)
    default = models.BooleanField(default=False)
    email = models.EmailField()
    full_name = models.CharField(max_length=200)
    phone = PhoneNumberField()
    sessionID = models.CharField(
        max_length=200,  null=True, blank=True)

    def __str__(self):

        return self.full_name

    class Meta:
        verbose_name_plural = 'Addresses'


# Payment Model Using stripe
class Payment(models.Model):
    orderRef = models.CharField(max_length=500)
    txRef = models.CharField(max_length=500)
    rave_ref = models.CharField(max_length=500)
    stripe_charge_id = models.CharField(max_length=50)
    user = models.ForeignKey(User,
                             on_delete=models.SET_NULL, related_name='payments', blank=True, null=True)
    amount = models.FloatField()
    currency = models.CharField(max_length=222)
    timestamp = models.DateTimeField(auto_now_add=True)
    sessionID = models.CharField(
        max_length=200,  null=True, blank=True)
    type = models.CharField(max_length=3, blank=True,
                            null=True, choices=(('O', 'Order'), ('R', 'Refund')))
    status = models.CharField(max_length=3, default='p', choices=(
        ('s', 'successful'), ('p', 'pending'), ('f', 'failed')))
    method = models.CharField(max_length=3, default='R', choices=(
        ('R', 'Rave Payment'),))

    def __str__(self):
        if self.user:
            return self.user.username
        if self.sessionID:
            return self.sessionID
        else:
            return f'{self.id}'


# Coupon Model
class Coupon(models.Model):
    code = models.CharField(max_length=15)
    amount = models.FloatField()

    def __str__(self):
        return self.code


# Refund Model
class Refund(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    reason = models.TextField()
    accepted = models.BooleanField(default=False)
    email = models.EmailField()

    def __str__(self):
        return f"{self.pk}"


class Review(models.Model):

    user = models.ForeignKey(
        User,  on_delete=models.CASCADE, related_name='album_reviews')
    review = models.TextField(max_length=5000)
    post = models.ForeignKey(
        Album, on_delete=models.CASCADE, related_name='reviews')
    replies = models.ManyToManyField(
        'Review', related_name='parent_review')
    name = models.CharField(max_length=100, blank=True, null=True)
    email = models.EmailField(max_length=100, blank=True, null=True)
    website = models.URLField(blank=True, null=True)
    rating = models.IntegerField(default=1)
    created_on = models.DateTimeField(auto_now_add=True)  # Date of creation
    updated_on = models.DateTimeField(auto_now=True)  # Date of updation

    def get_add_reply_url(self):
        return reverse('discography:reply-review', kwargs={'pk': self.pk})

    def get_delete_review_url(self):
        return reverse('discography:delete-review', kwargs={'pk': self.pk})


def gen_slug(sender, created, instance: Album, *args, **kwargs):
    if created:
        slug = slugify(instance.title)
        instance.slug = slug
        instance.save()


post_save.connect(gen_slug, sender=Album)


def gen_ref(sender, created, instance: Order, *args, **kwargs):
    if created:
        if not instance.ref_code:
            gen = True

            gen_ref_code = ''
            while gen == True:
                try:
                    gen_ref_code = gen_ref_code.join(random.choice(
                        string.ascii_uppercase + str(random.randint(0, 999999999999))) for i in range(10))
                    gen = False
                except:
                    gen = True
            instance.ref_code = gen_ref_code
            instance.save()


post_save.connect(gen_ref, sender=Order)


def address_default_Setting(sender, created, instance: Address, *args, **kwargs):
    if created:

        if instance.default == True:
            for address in Address.objects.all():
                if address.default == True and address.address_type == instance.address_type and address.user == instance.user or address.sessionID == instance.sessionID:
                    address.default = False
                    address.save()
            pass
        instance.default = True
        instance.save()


post_save.connect(address_default_Setting, sender=Address)
