from django.http import HttpResponse, HttpRequest
from django.shortcuts import render


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