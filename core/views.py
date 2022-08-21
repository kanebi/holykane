from django.utils import timezone
from django_countries import Countries
from events.models import Event
from media.models import Video, Gallery
from blog.models import BlogPost
from shop.models import Album
from django.contrib.auth.models import User
import uuid
from django.conf import settings
from django.forms import EmailField, ValidationError
from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.mail import send_mail
from .models import ContactUs, Newsletter
from discography.models import Song
# Create your views here.


def get_session_id(request):
    sessionId = request.session.get('sessionID')
    if not request.user.is_authenticated:
        sessionId = request.session.get('sessionID')
        if not sessionId:
            sessionId = uuid.uuid1().hex
            request.session.__setitem__('sessionID', sessionId)
    return sessionId


def profile(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        print(request.POST)
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        phone = request.POST.get('phone')
        country = request.POST.get('country')
        emailCheck = User.objects.all().filter(email=email)
        if emailCheck.exists() and email != request.user.email:
            messages.error(request, 'Email already exists', 'error')
        else:
            if request.user.is_authenticated:
                user = request.user
                user.email = email if email else ''
                user.first_name = first_name if first_name else ''
                user.last_name = last_name if last_name else ''
                user.save()
                user.profile.phone = phone
                user.profile.country = country
                user.profile.save()
                if request.FILES:
                    print(request.FILES)
                    user.profile.picture = request.FILES.get('picture')
                    user.profile.save()
                messages.success(request, 'Profile Saved', 'success')
    context = {}
    context['countries'] = Countries()
    return render(request, 'core/profile.html', context)


def about(request):
    return render(request, 'core/about.html')


def contact(request):
    if request.method == 'POST':
        sender_email = request.POST.get('your-email')
        subject = request.POST.get('your-subject')
        name = request.POST.get('your-name')
        message = request.POST.get('your-message')
        contact = ContactUs()
        contact.email = sender_email
        contact.sender_name = name
        contact.subject = subject
        contact.message = message
        contact.save()
        mail = send_mail(sender_email + subject, message, settings.EMAIL_HOST_USER, [
                         'emmakanebi@gmail.com'])
        messages.success(
            request, 'Your Message was successfully sent. You will get a response before 24hrs!', extra_tags='success')
        return redirect('/')
    return render(request, 'core/contact.html')


def index(request):
    eShop = Album.objects.all().order_by('?')[0:3]
    blog = BlogPost.objects.all().order_by('?')[0:3]
    photo_gallery = Gallery.objects.all().order_by('?')[0:3]
    videos = Video.objects.all().order_by('?')[0:3]
    up_events = Event.objects.all().filter(
        date_time__gte=timezone.now())[0:6]
    context = {
        'eShop': eShop,
        'blogPosts': blog,
        'photo_galleries': photo_gallery,
        'videos': videos,
        'upcoming_events': up_events,
        'shuffle_songs': Song.objects.all().order_by('-created_on')[:5],
    }
    get_session_id(request)
    return render(request, 'core/index.html', context)


def newsletter_signin(request):
    context = {}
    if request.method == 'POST':
        f = EmailField()
        req_email = request.POST.get('email')
        if req_email:
            try:
                f.clean(req_email)
            except ValidationError:
                messages.error(request, 'Invalid email', extra_tags='error')
                return redirect('.')
            nwL = Newsletter.objects.filter(email=req_email)
            if nwL.exists():
                if nwL[0].subscribed == True:

                    messages.info(
                        request, 'Email already in our list. ', extra_tags='info')

                    return redirect('.')
                else:
                    nwL = Newsletter.objects.get(id=nwL[0].id)

                    nwL.subscribed = True

                    nwL.save()
                    messages.success(
                        request, 'Thank you for signing up to our newsletter! ', extra_tags='success')

                    return redirect('.')
            else:
                nwL = Newsletter.objects.create(email=req_email, )
                messages.success(
                    request, 'Thank you for signing up to our newsletter! ', extra_tags='success')

                return redirect('/')
        else:
            messages.info(request, 'No email entered !')
            return redirect('.')

    return render(request, 'core/newsletter.html')


def newsletter_signout(request):
    context = {}
    if request.method == 'POST':
        f = EmailField()
        req_email = request.POST.get('email')
        if req_email:
            try:
                f.clean(req_email)
            except ValidationError:
                messages.error(request, 'Invalid email', extra_tags='error')
                return redirect('.')
            nwL = Newsletter.objects.filter(email=req_email)
            if nwL.exists():
                nwL = Newsletter.objects.get(id=nwL[0].id)
                nwL.subscribed = False

                nwL.save()
                messages.info(
                    request, "Signout Complete, it's hard to say goodbye.. ", extra_tags='info')

                return redirect('/')
            else:

                messages.error(request, 'Email not Found ', extra_tags='error')

                return redirect('.')
        else:
            messages.info(request, 'No email entered !')
            return redirect('.')

    return render(request, 'core/newsletter-signout.html')
