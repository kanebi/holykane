import uuid
from django.template import Library
from shop.models import Cart

from core.models import SHIPPING_FEE
register = Library()


@register.filter()
def get_user_cart(request):

    sessionId = request.session.get('sessionID')
    if not sessionId:
        sessionId = uuid.uuid1().hex
        request.session.__setitem__('sessionID', sessionId)
    if request.user.is_authenticated:
        cart = request.user.carts.all().filter(ordered=False)
        return {
            'count': cart.count(),
            'total_sum': request.user.profile.get_cart_sub_total(),
            'final_total_sum': request.user.profile.get_cart_total(),
            'all': cart,
            'shipping_fee': SHIPPING_FEE,
        }
    else:
        cart = Cart.objects.all().filter(ordered=False, sessionID=sessionId)
        return {
            'count': cart.count(),
            'all': cart,
            'shipping_fee': SHIPPING_FEE,

            'total_sum': 0 if not cart.count() >= 1 else sum([item.get_final_sum_price() for item in cart]),
            'final_total_sum': 0 if not cart.count() >= 1 else sum([item.get_final_sum_price() for item in cart]) + SHIPPING_FEE

        }
