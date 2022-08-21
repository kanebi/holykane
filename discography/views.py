from tkinter.messagebox import NO
import uuid
from django.shortcuts import get_object_or_404, redirect, render
from django.db.models import Q, Count, Sum
from .models import Song
from shop.models import Review, Cart, Album
from django.core import paginator
from django.contrib import messages
from shop.views import shop
from shop.models import Album, ALBUM_CATEGORIES
from tkinter.messagebox import NO
import uuid
from django.shortcuts import get_object_or_404, redirect, render
from django.db.models import Q, Count, Sum
from .models import Song
from shop.models import Review, Cart, Album
from django.core import paginator
from django.contrib import messages
# Create your views here.
from core.views import get_session_id


def shop(request):
    eShop = Album.objects.all().order_by('-created_on')
    otherP = Album.objects.all().order_by('?')[:3]

    if str(request.GET.get('clr')) == 'True':
        request.session.__setitem__('orderby', 'default')
        request.session.__setitem__('min_price', 0)
        request.session.__setitem__('max_price', 100)

        return filter_products(request)

    paginated_qs = paginator.Paginator(eShop, 10)
    page_object_list = paginated_qs.page(1)
    page = request.GET.get('paged') if request.GET.get('paged') else 1
    if page:
        try:
            page_object_list = paginated_qs.page(page)
        except paginator.EmptyPage:
            page_object_list = paginated_qs.page(1)
        except paginator.PageNotAnInteger:
            page_object_list = paginated_qs.page(1)

    context = {

        'products': page_object_list,
        'page': page,
        'paginator': paginated_qs,
        'otherProducts': otherP,
        'orderby': 'default' if not request.session.get('orderby') else request.session.get('orderby'),
        'min_price': 0 if not request.session.get('min_price') else request.session.get('min_price'),
        'max_price': 100 if not request.session.get('max_price') else request.session.get('max_price')
        # 'max_price': '100'

    }
    if str(request.GET.get('flt')) == 'True':
        return filter_products(request)

    return render(request, 'discography/shop.html', context=context)


def filter_products(request):
    eShop = Album.objects.all().order_by('-created_on')
    otherP = Album.objects.all().order_by('?')[:3]
    orderBy = 'default' if not request.GET.get(
        'orderby') else request.GET.get('orderby')
    min_price = 0 if not request.GET.get(
        'min_price') else request.GET.get('min_price')
    max_price = 100 if not request.GET.get(
        'max_price') else request.GET.get('max_price')
    # print(min_price, max_price)

    if orderBy != 'default':

        request.session.__setitem__('orderby', orderBy)

    if max_price != 100:
        request.session.__setitem__('max_price', max_price)
    if min_price != 0:
        request.session.__setitem__('min_price', min_price)
    eShop = eShop.filter(price__gte=min_price,
                         price__lte=max_price)
    # print(min_price, max_price)
    if request.session.get('orderby') != 'default' and orderBy == 'default':
        orderBy = request.session.get('orderby')
    if request.session.get('min_price') != 0 and min_price == 0:
        min_price = request.session.get('min_price')

    if request.session.get('max_price') != 100 and max_price == 100:
        max_price = request.session.get('max_price')

    if orderBy == 'popularity':
        eShop = eShop.annotate(total_streams=Count(
            'songs__streams')).order_by('-total_streams')
    if orderBy == 'date':
        eShop = eShop.order_by('-created_on')
    if orderBy == 'rating':
        eShop = eShop.annotate(
            total_rating=Sum('reviews__rating')).order_by('-total_rating')
    if orderBy == 'price-desc':
        eShop = eShop.order_by('-price')
    if orderBy == 'price':
        eShop = eShop.order_by('price')
    paginated_qs = paginator.Paginator(eShop, 10)
    page_object_list = paginated_qs.page(1)
    page = request.GET.get('paged')
    if page:
        try:
            page_object_list = paginated_qs.page(page)
        except paginator.EmptyPage:
            page_object_list = paginated_qs.page(1)
        except paginator.PageNotAnInteger:
            page_object_list = paginated_qs.page(1)
    context = {
        'products': page_object_list,
        'paginator': paginated_qs,
        'otherProducts': otherP,
        'orderby': orderBy,
        'min_price': min_price,
        'query': True,
        'max_price': max_price,
        'page': page,
        # 'max_price': '100'
    }

    return render(request, 'layouts/products_list.html', context=context)


def add_toFav(request, album_pk, song_pk):

    album = get_object_or_404(Album, pk=album_pk)
    sessionId = request.session.get('sessionID')
    if not sessionId:
        sessionId = uuid.uuid1().hex
        request.session.__setitem__('sessionID', sessionId)
    if request.user.is_authenticated:

        albumFav = album.faved.all().filter(
            user=request.user, album=album)
        if albumFav.exists():
            albumFav = albumFav[0]
            if song_pk == 'all':
                albumFav.songs.set([song.id for song in album.songs.all()])
            else:
                songCheck = albumFav.songs.filter(pk=song_pk)
                if songCheck.exists():
                    albumFav.songs.remove(songCheck[0])
                else:
                    if albumFav.songs.count() == 0 and song_pk == 'none':
                        albumFav.delete()
                    else:
                        albumFav.songs.add(Song.objects.get(pk=song_pk))
        else:
            albumFav = album.faved.create(
                user=request.user,  album=album, )
            if song_pk == 'all':
                albumFav.songs.set([song.id for song in album.songs.all()])
            else:
                albumFav.songs.add(Song.objects.get(pk=song_pk))
    else:

        albumFav = album.faved.all().filter(
            sessionID=sessionId, album=album)
        if albumFav.exists():
            albumFav = albumFav[0]
            if song_pk == 'all':
                albumFav.songs.set([song.id for song in album.songs.all()])
            else:
                songCheck = albumFav.songs.filter(pk=song_pk)
                if songCheck.exists():
                    albumFav.songs.remove(songCheck[0])
                else:
                    if albumFav.songs.count() == 0 and song_pk == 'none':

                        albumFav.delete()
                    else:
                        albumFav.songs.add(Song.objects.get(pk=song_pk))
        else:
            albumFav = album.faved.create(
                sessionID=sessionId,  album=album, )
            if song_pk == 'all':
                albumFav.songs.set([song.id for song in album.songs.all()])
            else:
                albumFav.songs.add(Song.objects.get(pk=song_pk))

    return redirect(album.get_absolute_url())


def update_streams(request, pk):
    song = get_object_or_404(Song, pk=pk)

    sessionId = request.session.get('sessionID')
    if not sessionId:
        sessionId = uuid.uuid1().hex
        request.session.__setitem__('sessionID', sessionId)

    songStream = song.streams.get_or_create(
        user=request.user, sessionID=sessionId, song=song)
    songStream[0].count += 1
    songStream[0].save()
    return redirect(song.audio.url)


def update_downloads(request, pk):
    song = get_object_or_404(Song, pk=pk)

    sessionId = request.session.get('sessionID')
    if not sessionId:
        sessionId = uuid.uuid1().hex
        request.session.__setitem__('sessionID', sessionId)

    songDownloads = song.downloads.get_or_create(
        user=request.user, sessionID=sessionId, song=song)
    songDownloads[0].count += 1
    songDownloads[0].save()
    return redirect(song.audio.url)


def songDetail(request, pk, slug):
    album = get_object_or_404(Album, pk=pk, slug=slug)
    context = {
        'related_songs': Album.objects.filter(genre__name__contains=album.genre.name),
        'album': album

    }

    return render(request, 'discography/song-detail.html', context)


def productDetail(request, pk, slug):
    product = get_object_or_404(Album, pk=pk, slug=slug)
    context = {
        'related_products': Album.objects.filter(genre__name__contains=product.genre.name),
        'products': Album.objects.all().order_by('?').exclude(id=product.id),
        'product': product

    }
    return render(request, 'discography/product-detail.html', context)


def searched(request):
    query = request.GET.get('q')

    eShop = Album.objects.all().filter(Q(title__contains=query) | Q(songs__title=query) | Q(
        keywords=query) | Q(songs__producers__name__contains=query))
    otherP = Album.objects.all().order_by('?')[:3]

    if str(request.GET.get('clr')) == 'True':
        request.session.__setitem__('orderby', 'default')
        request.session.__setitem__('min_price', 0)
        request.session.__setitem__('max_price', 100)

        return filter_products(request)

    paginated_qs = paginator.Paginator(eShop, 10)
    page_object_list = paginated_qs.page(1)
    page = request.GET.get('paged') if request.GET.get('paged') else 1
    if page:
        try:
            page_object_list = paginated_qs.page(page)
        except paginator.EmptyPage:
            page_object_list = paginated_qs.page(1)
        except paginator.PageNotAnInteger:
            page_object_list = paginated_qs.page(1)

    context = {
        'query': query,
        'products': page_object_list,
        'page': page,
        'paginator': paginated_qs,
        'otherProducts': otherP,
        'orderby': 'default' if not request.session.get('orderby') else request.session.get('orderby'),
        'min_price': 0 if not request.session.get('min_price') else request.session.get('min_price'),
        'max_price': 100 if not request.session.get('max_price') else request.session.get('max_price')
        # 'max_price': '100'

    }

    if str(request.GET.get('flt')) == 'True':
        return filter_products(request)

    return render(request, 'discography/searches.html', context)


def add_to_cart(request, slug):
    try:
        product = get_object_or_404(Album, slug=slug)
        if request.user.is_authenticated:
            cart = Cart.objects.get_or_create(
                user=request.user, item=product)[0]
        else:

            sessionId = request.session.get('sessionID')
            if not sessionId:
                sessionId = uuid.uuid1
                request.session.__setitem__('sessionID', sessionId)
            cart = Cart.objects.get_or_create(
                sessionID=sessionId, item=product)[0]
        if request.method == 'POST':

            qty = request.POST.get('quantity')
            if qty and int(qty) >= 1:
                cart.item = product
                cart.quantity = qty
                cart.save()
                messages.success(request, 'Cart updated.',
                                 extra_tags='success')

            else:
                cart.item = product
                cart.save()
        else:
            quantity = request.GET.get('quantity')
            if quantity and str(quantity).isnumeric() and int(quantity) >= 1:
                cart.quantity = quantity
                cart.save()
                return redirect('shop:cart')
    except TypeError as e:
        messages.error(request, 'invalid entry',
                       extra_tags='error')
        return redirect('shop:cart')
    return redirect(product.get_shop_url())


def remove_from_cart(request, slug):
    product = get_object_or_404(Album, slug=slug)
    if request.user.is_authenticated:
        cart = Cart.objects.get_or_create(
            user=request.user, item=product)[0]
    else:

        sessionId = request.session.get('sessionID')
        if not sessionId:
            sessionId = uuid.uuid1
            request.session.__setitem__('sessionID', sessionId)
        cart = Cart.objects.get_or_create(
            sessionID=sessionId, item=product)[0]

    cart.delete()

    messages.success(request, 'Product removed from cart.',
                     extra_tags='success')

    return redirect('/shop/cart')


def add_review_url(request, product_id):
    if request.method == 'POST':
        review = Review()
        product = get_object_or_404(Album, id=product_id)

        if str(request.POST.get('comment_parent')).isnumeric():
            commentId = request.POST.get('comment_parent')
            targetReview = get_object_or_404(Review, id=commentId)
            if not request.user.is_authenticated:
                review.name = request.POST.get('name')
                review.review = request.POST.get('comment')
                review.email = request.POST.get('email')
                review.rating = request.POST.get('rating')
                review.post = product
                review.save()

            else:
                review.user = request.user
                review.review = request.POST.get('comment')
                review.name = request.user.username
                review.email = request.user.email
                review.rating = request.POST.get('rating')
                review.post = product
                review.save()
            targetReview.replies.add(review)
            messages.success(request, 'Post replied', extra_tags='success')

        else:
            if not request.user.is_authenticated:
                review.name = request.POST.get('name')
                review.review = request.POST.get('comment')
                review.email = request.POST.get('email')
                review.rating = request.POST.get('rating')
                review.post = product
                review.save()
            else:
                review.user = request.user

                review.review = request.POST.get('comment')
                review.rating = request.POST.get('rating')
                review.name = request.user.username
                review.email = request.user.email
                review.post = product
                review.save()
                messages.success(request, 'Review Posted',
                                 extra_tags='success')
    return redirect(product.get_shop_url())


def products_by_category(request, category):

    context = {
        'related_products': Album.objects.filter(category=category),

    }

    return redirect('.')


def discoMasonary(request):

    context = {
        'albums': Album.objects.all(),
        'album_categories': ALBUM_CATEGORIES,

    }

    return render(request, 'discography/disco-masonary.html', context)


def discoAll(request):

    context = {
        'albums': Album.objects.all(),

    }
    return render(request, 'discography/disco-all.html', context)


def index(request):
    context = {}
    return render(request, 'discography/index.html', context=context)


def remove_from_wish(request, type, pk):
    sessionId = get_session_id(request)
    if type == 'song':
        song = Song.objects.get(pk=pk)

        if request.user.is_authenticated:

            songFav = song.favs.all().filter(
                user=request.user)
            if songFav.exists():
                songFav[0].songs.remove(song)
        else:

            songFav = song.favs.all().filter(
                sessionID=sessionId)
            if songFav.exists():
                songFav[0].songs.remove(song)

    return redirect('shop:wishlist')
