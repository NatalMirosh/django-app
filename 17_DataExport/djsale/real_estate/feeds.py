from django.contrib.syndication.views import Feed
from django.urls import reverse
from .models import News


class NewsFeed(Feed):
    title = 'My News Feed'
    link = '/real_estate/news/'
    description = 'Latest news from my website'

    def items(self):
        return News.objects.order_by('-pub_date')[:10]

    def item_title(self, item):
        return item.title

    def item_description(self, item):
        return item.content

    def item_link(self, item):
        return reverse('real_estate:news_list')