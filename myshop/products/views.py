from django.shortcuts import render, get_object_or_404

from .models import Product, Category
from cart.forms import CartAddForms


def product_list(request, category_slug=None):
    category = None
    categories = Category.objects.all()
    products = Product.objects.filter(available=True)
    if category_slug:
        category = get_object_or_404(Category,
                                     slug=category_slug)
        products = Product.objects.filter(category=category)
    return render(request,
                  'products/product/list.html',
                  {'products': products,
                   'categories': categories,
                   'category': category})


def product_detail(request, id, product_slug):
    product = get_object_or_404(Product,
                                id=id,
                                slug=product_slug)
    cart_product_form = CartAddForms()
    return render(request, 'products/product/detail.html',
                  {'product': product,
                   'cart_product_form': cart_product_form})
