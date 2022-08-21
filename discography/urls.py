
from django.contrib import admin
from django.urls import path, include

from discography.views import filter_products, remove_from_wish, remove_from_cart, discoMasonary, discoAll, songDetail, index, add_toFav, productDetail, shop, searched, add_to_cart, products_by_category, add_review_url, update_downloads, update_streams


app_name = 'discography'
urlpatterns = [
    path('shop/', shop, name='shop'),
    path('p/<pk>/<slug>', productDetail, name='product-detail'),
    path('album/<pk>/<slug>', songDetail, name='album-detail'),
    path('album/p/search/', searched, name='search'),
    path('album/p/add-to-cart/<slug>/', add_to_cart, name='add-to-cart'),
    path('album/p/remove-from-cart/<slug>/',
         remove_from_cart, name='remove-from-cart'),
    path('album/p/add-review/<product_id>',
         add_review_url, name='add-review'),
    path('album/products-by-category/<category>/',
         products_by_category, name='products-by-category'),
    path('track/update-streams/<pk>/', update_streams, name='update-streams'),
    path('track/update-downloads/<pk>/',
         update_downloads, name='update-downloads'),
    path('track/favourite/<album_pk>/<song_pk>/',
         add_toFav, name='add-to-fav'),
    path('', index, name='home'),
    path('p/filter/', filter_products, name='product-filter'),
    path('masonry/', discoMasonary, name='masonry'),
    path('all', discoAll, name='all'),
    path('remove-from-wish/<type>/<pk>/',
         remove_from_wish, name='remove-from-wish'),

]
