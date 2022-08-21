from django.contrib import admin
from .models import Slides, HomePage, ContactPage, ContactUs, UserProfile
# Register your models here.


admin.site.register([Slides, HomePage, ContactPage, ContactUs, UserProfile])
