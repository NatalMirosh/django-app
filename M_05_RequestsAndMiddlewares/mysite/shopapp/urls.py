from django.urls import path
from .views import shop_index, products_list, orders_list

app_name = "blogapp"

urlpatterns = [
    path("", shop_index, name = 'index'),
    path("products/", products_list, name='products_list'),
    path("orders/", orders_list, name='orders_list'),

]