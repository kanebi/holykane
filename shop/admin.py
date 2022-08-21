from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Album, Address, Order, Cart, Review, Refund,  FileManager, Payment, Favourite
# Register your models here.
admin.site.register([

    Album, Address, Order, Cart, Review, Refund,  FileManager, Payment, Favourite

])
