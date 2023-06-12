from django.http import HttpResponse, HttpRequest
from django.shortcuts import render

from .models import Product, Order

def shop_index(request: HttpRequest):
    products = [
        ('Orange', 55),
        ('Bananas', 130),
        ('Ananas', 100),
    ]

    context = {
        'products': products
    }



    return render(request, 'blogapp/shop-index.html', context=context)

def products_list(request: HttpRequest):
    context = {
        "products": Product.objects.all(),
    }
    return render(request, 'blogapp/products-list.html', context=context)


def orders_list(request: HttpRequest):
    context = {
        "orders": Order.objects.select_related("user").prefetch_related("products").all(),
    }
    return render(request, 'blogapp/order_list.html', context=context)