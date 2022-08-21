
from django.contrib import admin
from django.urls import path, include
from .views import eventByCategory, eventDetail, events, eventsAll

app_name = 'events'
urlpatterns = [

    path('category/<category>', eventByCategory, name='category'),
    path('detail/<pk>', eventDetail, name='detail'),
    path('', events, name='events-masonry'),
    path('all/', eventsAll, name='events-all'),
]
