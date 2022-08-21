from decimal import Decimal
from decouple import config
import json
import uuid
from django.conf import settings
from django.http import HttpResponse, QueryDict
from django.shortcuts import get_object_or_404, redirect, render
from django.db.models import Q, Count, Sum
from .models import Song
from shop.models import Review, Cart, Album, Order, Payment, Address
from django.core import paginator
from django.contrib import messages
from core.views import get_session_id
from django.utils import timezone
from .forms import ShippingAddressesForm, BillingAddressesForm
# Create your views here.


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
        print('true')
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
    paginated_qs = paginator.Paginator(eShop, 1)
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


def cart(request):
    return render(request, 'shop/cart.html')


def create_order(request, shipping_addr, billing_adr=None, in_app=False):

    if request.user.is_authenticated:

        carts = request.user.carts.all().filter(ordered=False)
        order = request.user.orders.all().get_or_create(
            items__in=carts, user=request.user, ordered=False)[0]

    else:
        carts = Cart.objects.all().filter(ordered=False, sessionID=get_session_id(request))

        # order.sessionID = get_session_id(request)
        order = Order.objects.all().get_or_create(
            items__in=carts, sessionID=get_session_id(request), ordered=False)[0]

    order.shipping_address = get_object_or_404(Address, id=shipping_addr)
    if billing_adr:
        order.billing_address = get_object_or_404(Address, id=billing_adr)
    else:
        order.billing_address = get_object_or_404(Address, id=shipping_addr)

    order.save()
    order.items.set(carts)
    if in_app == True:
        return payment(request, type='order-create', order_id=order.id)
    else:
        return redirect('shop:payment', type='order-create', order_id=order.id)


def checkout(request):
    sessionId = get_session_id(request)
    if request.user.is_authenticated:
        if not request.user.carts.all().filter(ordered=False, ).exists():
            return redirect('shop:cart')

        default_sh_address = request.user.addresses.all().filter(
            default=True, address_type='S')
        default_bl_address = request.user.addresses.all().filter(
            default=True, address_type='B')
    else:
        if not Cart.objects.all().filter(ordered=False, sessionID=sessionId).exists():
            return redirect('shop:cart')

        default_sh_address = Address.objects.all().filter(
            default=True, sessionID=sessionId, address_type='S')
        default_bl_address = Address.objects.all().filter(
            default=True, sessionID=sessionId,  address_type='B')

    default_sh_address = None if not default_sh_address.exists(
    ) else default_sh_address[0]
    default_bl_address = None if not default_bl_address.exists(
    ) else default_bl_address[0]

    if not request.user.is_authenticated:
        shippingAddressForm = ShippingAddressesForm()
        billingAddressForm = BillingAddressesForm()
    else:

        shippingAddressForm = ShippingAddressesForm(
            data={'email': request.user.email, 'full_name': f'{request.user.first_name} {request.user.last_name}'})
        billingAddressForm = BillingAddressesForm(
            data={'email': request.user.email, 'full_name': f'{request.user.first_name} {request.user.last_name}'})

    context = {
        'billing_form': billingAddressForm,
        'shipping_form': shippingAddressForm,
        'default_billing_address': default_bl_address,
        'default_shipping_address': default_sh_address
    }
    if request.method == 'POST':
        # print(request.POST)
        no_billing = request.POST.get('no_billing')

        if request.POST.get('use_default_shipping') == 'true' and request.POST.get('use_default_billing') == 'true':

            return create_order(request, default_sh_address.id, default_bl_address.id, in_app=True)
        else:
            if request.POST.get('use_default_shipping') == 'true' and request.POST.get('use_default_billing') == 'false':
                if no_billing == 'true':
                    return create_order(request, default_sh_address.id,  in_app=True)

                else:
                    loaded_bl_form = json.loads(
                        request.POST.get('billing_form'))
                    billingForm = BillingAddressesForm(loaded_bl_form)
                    if billingForm.is_valid():
                        bl_address = billingForm.save(commit=False)
                        if request.user.is_authenticated:
                            bl_address.user = request.user
                            bl_address.save()
                        else:
                            bl_address.sessionID = sessionId
                            bl_address.save()
                    return create_order(request, default_sh_address.id, bl_address.id, in_app=True)
            if request.POST.get('use_default_shipping') == 'false' and request.POST.get('use_default_billing') == 'true':
                loaded_sh_form = json.loads(request.POST.get('shipping_form'))
                shippingForm = ShippingAddressesForm(loaded_sh_form)
                if shippingForm.is_valid():
                    sh_address = shippingForm.save(commit=False)
                    if request.user.is_authenticated:
                        sh_address.user = request.user
                        sh_address.save()
                    else:
                        sh_address.sessionID = sessionId
                        sh_address.save()
                return create_order(request, sh_address.id, default_bl_address.id,  in_app=True)

        loaded_sh_form = json.loads(request.POST.get('shipping_form'))
        shippingForm = ShippingAddressesForm(loaded_sh_form)

        if no_billing == 'true':
            if shippingForm.is_valid():
                shipping_formInst = shippingForm.save(commit=False)
                if request.user.is_authenticated:
                    shipping_formInst.user = request.user
                    shipping_formInst.save()

                else:
                    shipping_formInst.sessionID = sessionId
                    shipping_formInst.save()
                return create_order(request, shipping_formInst.id, in_app=True)

            else:
                messages.error(request, shippingForm.errors,
                               extra_tags='error')
                context['form_errors'] = shippingForm.non_field_errors()
        else:
            loaded_bl_form = json.loads(
                request.POST.get('billing_form'))
            billingForm = BillingAddressesForm(loaded_bl_form)
            if billingForm.is_valid():
                shipping_formInst = shippingForm.save(commit=False)
                billing_formInst = billingForm.save(commit=False)
                if request.user.is_authenticated:
                    shipping_formInst.user = request.user
                    shipping_formInst.save()
                    billing_formInst.user = request.user
                    billing_formInst.save()
                else:
                    shipping_formInst.sessionID = sessionId
                    shipping_formInst.save()
                    billing_formInst.sessionID = sessionId
                    billing_formInst.save()
                return create_order(request, shipping_formInst.id,
                                    billing_formInst.id, in_app=True)
            else:
                messages.error(request, billingForm.errors,
                               extra_tags='error')
                context['form_errors'] = f'{billingForm.non_field_errors()} {shippingForm.non_field_errors()}'

    return render(request, 'shop/checkout.html', context)


def wishlist(request):

    return render(request, 'shop/wishlist.html')


def order(request):
    context = {}

    orders = Order.objects.filter(Q(user=request.user if request.user.is_authenticated else None) | Q(
        sessionID=get_session_id(request))).filter(ordered=True)
    context['orders'] = orders
    return render(request, 'shop/order.html', context)


def order_detail(request, code):
    context = {}
    if code:
        order = get_object_or_404(Order, ref_code=code)
        context['order'] = order
    return render(request, 'shop/order-detail.html', context)


def payment_status(request,  order_code):
    context = {}
    response = request.GET.get('response')
    order = get_object_or_404(Order, ref_code=order_code)
    if response:
        resp = json.loads(response)
        status = resp['status']
        if status == 'successful' and (str(order.get_total().amount) == str(resp['charged_amount']) and str(order.get_total().currency) == str(resp['currency'])):
            order.payment.status = 's'
            order.payment.rave_ref = resp['raveRef']
            order.payment.amount = resp['charged_amount']
            order.payment.currency = resp['currency']
            order.payment.orderRef = resp['orderRef']
            order.payment.txRef = resp['txRef']
            order.payment.save()
            order.status = 'P'
            for items in order.items.all():
                items.ordered = True
                items.save()
            order.ordered_date = timezone.now()
            order.ordered = True
            order.save()
        else:
            order.payment.status = resp['status'][0]
            order.payment.rave_ref = resp['raveRef']
            order.payment.amount = resp['charged_amount']
            order.payment.currency = resp['currency']
            order.payment.orderRef = resp['orderRef']
            order.payment.txRef = resp['txRef']
            order.payment.save()

    context['order'] = order

    return render(request, 'shop/payment-status.html', context)


def payment(request, type,  order_id=None):
    context = {}
    if type == 'order-create':

        order = get_object_or_404(Order, id=order_id)

        if request.user.is_authenticated:
            payment = request.user.payments.all(
            ).get_or_create(order__id=order.id, user=request.user, currency=order.get_total().currency, type='O', amount=order.get_total().amount)[0]
        else:
            payment = Payment.objects.all(
            ).get_or_create(sessionID=get_session_id(request), type='O', currency=order.get_total().currency, amount=order.get_total().amount, order__id=order.id)[0]
        order.payment = payment
        order.save()
        context['order'] = order
        context['flutter_key'] = settings.FLUTTERWAVE_PUBLIC_KEY

    return render(request, 'shop/payment.html', context)
