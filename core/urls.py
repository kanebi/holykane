
from django.contrib import admin
from django.urls import path, include
from .views import index, newsletter_signin, newsletter_signout, about, contact, profile
from discography.views import shop
urlpatterns = [
    path('', index, name='home'),
    path('newsletter-signin/', newsletter_signin, name='newsletter_signin'),
    path('newsletter-signout/', newsletter_signout, name='newsletter_signout'),
    path('about-holykane-solo/', about, name='about'),
    path('contact/', contact, name='contact'),
    path('shop/', shop, name='shop'),
    path('my-account/', profile, name='Profile'),
]
