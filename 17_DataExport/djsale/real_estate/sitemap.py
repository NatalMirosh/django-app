from django.contrib.sitemaps import Sitemap
from django.urls import reverse
from .models import News


# class StaticViewSitemap(Sitemap):
#     def items(self):
#         return ['contacts', 'about', 'property_list']
#
#     def lastmod(self, item):
#         return item


class NewsSitemap(Sitemap):
    changefreq = 'weekly'
    priority = 0.3
    def items(self):
        return News.objects.all()

    def lastmod(self, item: News):
        return item.pub_date
