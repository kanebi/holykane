from django.shortcuts import render, get_object_or_404
from .models import Event, EVENT_CATEGORIES
from django.utils import timezone

# Create your views here.


def eventDetail(request, pk):
    event = get_object_or_404(Event, pk=pk)
    context = {
        'event': event
    }
    return render(request, 'events/event-detail.html', context)


def eventByCategory(request, category):
    events = Event.objects.all().filter(category=category)
    context = {
        'events': events
    }
    return render(request, 'events/event-category.html', context)


def events(request):
    upcoming_events = Event.objects.all().filter(date_time__gte=timezone.now())
    past_events = Event.objects.all().filter(date_time__lt=timezone.now())
    context = {
        'upcoming_events': upcoming_events,
        'past_events': past_events,
        'event_categories': EVENT_CATEGORIES,
    }
    return render(request, 'events/events-masonary.html', context)


def eventsAll(request):
    upcoming_events = Event.objects.all().filter(date_time__gte=timezone.now())
    past_events = Event.objects.all().filter(date_time__lt=timezone.now())
    context = {
        'upcoming_events': upcoming_events,
        'past_events': past_events
    }
    return render(request, 'events/events-all.html', context)
