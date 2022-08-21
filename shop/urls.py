
from django.urls import path, re_path
from .views import order, order_detail, payment_status, payment,  cart, checkout, wishlist

app_name = 'shop'

urlpatterns = [
    path('order/', order, name='order'),
    path('order-detail/<code>/', order_detail, name='order-detail'),
    path('order/<order_code>/',
         payment_status, name='payment-status'),
    path('cart/', cart, name='cart'),
    path('wishlist/', wishlist, name='wishlist'),
    path('checkout/', checkout, name='checkout'),
    path('payment/<type>/<order_id>/', payment, name='payment'),
]
