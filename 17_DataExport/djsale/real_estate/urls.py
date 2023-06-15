from django.urls import path
from .views import ContactsView, NewsListView, AboutView, PropertyListView
from .feeds import NewsFeed
from django.contrib.sitemaps.views import sitemap
from .sitemap import NewsSitemap

app_name = 'real_estate'

sitemaps = {
    'news': NewsSitemap,
}

urlpatterns = [
    path("news/", NewsListView.as_view(), name='news_list'),
    path("news/feed/", NewsFeed(), name='news_feed'),
    path("sitemap.xml", sitemap, {'sitemaps': sitemaps}, name='django.contrib.sitemaps.views.sitemap'),

    path("contacts/", ContactsView.as_view(), name='real_estate:contacts'),
    path("about/", AboutView.as_view(), name='about'),
    path("property_list/", PropertyListView.as_view(), name='property_list'),
]