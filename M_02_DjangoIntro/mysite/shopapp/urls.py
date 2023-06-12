from django.urls import path
from .views import shop_index

app_name = "blogapp"

urlpatterns = [
    path("", shop_index, name = 'index'),
]