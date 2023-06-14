from django.shortcuts import render
from django.views import View
from django.views.generic import TemplateView

from estates.models import News


class NewsListView(TemplateView):
    template_name = "estates/news_list.html"
