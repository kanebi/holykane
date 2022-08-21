from django.template.library import Library
from shop.models import Album, Favourite
import uuid
register = Library()


@register.filter()
def get_latest_EP(request):

    album = Album.objects.all().filter(category='E')
    if album.count() >= 1:
        return album.earliest('release_date')
    return album


@register.filter()
def get_user_favourites(request):
    if request.user.is_authenticated:
        favs = request.user.favourite_songs.all()

    else:
        sessionId = request.session.get('sessionID')
        if not sessionId:
            sessionId = uuid.uuid1().hex
            request.session.__setitem__('sessionID', sessionId)
        favs = Favourite.objects.all().filter(sessionID=sessionId)
    return favs
