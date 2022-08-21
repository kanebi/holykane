import io
import os
import random
import uuid
from django.conf import settings
from django.template.library import Library
from ..models import ContactPage, HomePage, Slides, AboutPage, Header
from django.core.files.base import ContentFile
from discography.models import Song
from pathlib import Path

register = Library()


@register.filter()
def get_header(request):
    header = Header.objects.get_or_create(
        name_id='default')[0]

    if not header.logo:
        header
        with open('static/logo.png', 'rb') as file:
            # imgFile = bytearray(file)
            header.logo.save('d-logo.png', file)
            header.save()
            file.close()
    return header


@register.filter()
def get_about_page(request):
    about_detail = AboutPage.objects.get_or_create(name_id='default')[0]
    if not about_detail.title:
        about_detail.title = 'About Holykane Solo'
    if not about_detail.description:
        about_detail.description = """
                        <p><img loading="lazy" class="alignleft size-medium wp-image-41" src="../wp-content/uploads/sites/2/2014/09/event1-300x200.jpg" alt="event1" width="300" height="200" srcset="https://www.cssigniter.com/vip/solo/wp-content/uploads/sites/2/2014/09/event1-300x200.jpg 300w, https://www.cssigniter.com/vip/solo/wp-content/uploads/sites/2/2014/09/event1.jpg 750w, https://www.cssigniter.com/vip/solo/wp-content/uploads/sites/2/2014/09/event1-350x235.jpg 350w, https://www.cssigniter.com/vip/solo/wp-content/uploads/sites/2/2014/09/event1-560x373.jpg 560w" sizes="(max-width: 300px) 100vw, 300px">Hymenaeos egestas conubia lacinia, ultrices porttitor gravida nunc ultrices massa dignissim velit tellus ridiculus ante nonummy magna. Pulvinar cum aenean nunc euismod nisi tortor mollis sociis phasellus metus pulvinar magnis et litora facilisis vel. Mus quis. Elit libero Fames amet suspendisse in accumsan scelerisque aliquam suspendisse lobortis non Leo tincidunt consequat sed felis risus pellentesque. Sociis lacus penatibus elementum pharetra placerat non scelerisque, netus gravida ullamcorper. Facilisi consectetuer felis id, sed dictumst ultrices potenti. Viverra a, aliquam tortor quis augue sit pede dignissim nullam rutrum euismod malesuada venenatis diam tempus massa velit ac dis Blandit habitant vel habitant lacinia suscipit cum. Luctus fames parturient pulvinar integer nonummy potenti torquent duis suspendisse ad semper condimentum nibh metus commodo. Ligula phasellus ac suscipit nostra ultrices ligula. Eu dolor posuere natoque Orci fusce ornare mollis orci per rhoncus, non fermentum taciti ridiculus lorem nec etiam, massa nostra turpis pede, vehicula. Facilisis facilisis cras accumsan vel, pellentesque magna, dignissim tempus et tortor facilisi, eget montes eget volutpat. Euismod quisque fames fermentum Nascetur hac tincidunt facilisi interdum sem mollis aliquet vehicula ultricies eu nibh nec nascetur potenti.</p>
                        <h3>Video</h3>
                        <p><div class="fluid-width-video-wrapper fluid-width-video-preview fluid-width-video-preview-youtube" style="padding-top: 56.2667%; background-image: url(&quot;//img.youtube.com/vi/OG2eGVt6v2o/sddefault.jpg&quot;);"><div class="play-button"></div></div></p>
                        <p>Hymenaeos egestas conubia lacinia, ultrices porttitor gravida nunc ultrices massa dignissim velit tellus ridiculus ante nonummy magna. Pulvinar cum aenean nunc euismod nisi tortor mollis sociis phasellus metus pulvinar magnis et litora facilisis vel. Mus quis. Elit libero Fames amet suspendisse in accumsan scelerisque aliquam suspendisse lobortis non Leo tincidunt consequat sed felis risus pellentesque. Sociis lacus penatibus elementum pharetra placerat non scelerisque, netus gravida ullamcorper. Facilisi consectetuer felis id, sed dictumst ultrices potenti. Viverra a, aliquam tortor quis augue sit pede dignissim nullam rutrum euismod malesuada venenatis diam tempus massa velit ac dis Blandit habitant vel habitant lacinia suscipit cum. Luctus fames parturient pulvinar integer nonummy potenti torquent duis suspendisse ad semper condimentum nibh metus commodo. Ligula phasellus ac suscipit nostra ultrices ligula. Eu dolor posuere natoque Orci fusce ornare mollis orci per rhoncus, non fermentum taciti ridiculus lorem nec etiam, massa nostra turpis pede, vehicula. Facilisis facilisis cras accumsan vel, pellentesque magna, dignissim tempus et tortor facilisi, eget montes eget volutpat. Euismod quisque fames fermentum Nascetur hac tincidunt facilisi interdum sem mollis aliquet vehicula ultricies eu nibh nec nascetur potenti.</p>
                   """
    about_detail.save()
    return about_detail


@register.filter()
def get_contact_page(request):
    contact_detail = ContactPage.objects.get_or_create(name_id='default', )

    return contact_detail[0]


@register.filter()
def get_homepage(request):

    slides = [{
        'name_id': 'default_1',
        'title': 'Banging New Track',
        'sub_title': 'Available for streaming on the platform',
        'location_url': '/',
        'action_text': 'View Track',
        'image': 'static/slides/slide_1.jpg'

    }, {
        'name_id': 'default_3',
        'title': 'Book  Online Today',
        'sub_title': 'Contact/Book Holykane Today! ',
        'location_url': '/',
        'action_text': 'Book Now',
        'image': 'static/slides/slide_2.jpg'

    }, {
        'name_id': 'default_2',
        'title': 'Shocking things you may not know about Holykane',
        'sub_title': 'Learn more about your favorite artist',
        'location_url': '/about',
        'action_text': "Okay, Let's Go",
        'image': 'static/slides/slide_3.jpg'

    },

    ]
    new_slides = []
    home_page = HomePage.objects.get_or_create(
        name_id='default')
    if home_page[0].slides.count() == 0:
        for slide in slides:
            sld = Slides.objects.get_or_create(**slide)
            with open(slide['image'], 'rb') as file:
                # imgFile = bytearray(file)
                sld[0].image.save(slide['image'].split('/')[-1], file)
                sld[0].save()
            file.close()
            new_slides.append(sld[0])
        home_page[0].slides.set(new_slides)
    if not home_page[0].recommended_tracks.all().count() >= 1:
        home_page[0].recommended_tracks.set(
            Song.objects.all().order_by('?')[:4])
    if not home_page[0].about_artist:
        home_page[
            0].about_artist = """  <p>Hymenaeos egestas conubia lacinia, ultrices porttitor gravida nunc ultrices massa dignissim velit tellus ridiculus ante nonummy magna. Pulvinar cum aenean nunc euismod nisi tortor mollis sociis phasellus metus pulvinar magnis et litora facilisis vel. Mus quis. Elit libero Fames amet suspendisse in accumsan scelerisque aliquam suspendisse lobortis non Leo tincidunt[&#8230;]</p> """
        with open(random.choice(slides)['image'], 'rb') as file:
            # imgFile = bytearray(file)
            home_page[0].about_artist_bg.save('default_abg.jpg', file)

            file.close()
        home_page[0].save()
    return home_page[0]


@register.filter()
def check_fav(request, songId):

    sessionId = request.session.get('sessionID')
    if not sessionId:
        sessionId = uuid.uuid1().hex
        request.session.__setitem__('sessionID', sessionId)
    track = Song.objects.get(id=songId)
    if request.user.is_authenticated:
        if track.favs.filter(user=request.user).exists():
            return True

    else:
        if track.favs.filter(sessionID=sessionId, ).exists():
            return True
    return False
