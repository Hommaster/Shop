from django.shortcuts import render, get_object_or_404, redirect
from django.views.decorators.http import require_POST

from .cart import Cart
from .forms import CartAddForms
from products.models import Product
from coupon.forms import CouponApplyForm


@require_POST
def cart_add(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    cart = Cart(request)
    form = CartAddForms(request.POST)
    if form.is_valid():
        cd = form.cleaned_data
        cart.add(product=product,
                 quantity=cd['quantity'],
                 override_quantity=cd['override'])
    return redirect('cart:cart_detail')


@require_POST
def cart_remove(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    cart = Cart(request)
    cart.remove(product)
    return redirect('cart:cart_detail')


def cart_detail(request):
    cart = Cart(request)
    coupon_apply_form = CouponApplyForm()
    for item in cart:
        item['update_quantity_form'] = CartAddForms(initial={
            'quantity': item['quantity'],
            'override': True
        })
    return render(request, 'cart/detail.html',
                  {'cart': cart,
                   'coupon_apply_form': coupon_apply_form})
