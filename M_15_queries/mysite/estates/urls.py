from django.urls import include, path

from .views import NewsListView

app_name = "estates"


urlpatterns = [
    path('news/', NewsListView.as_view(), name='news_list'),
]
