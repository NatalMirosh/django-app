from django.shortcuts import render
from django.views import View
from django.views.generic import TemplateView, ListView

from .models import RealEstate, News


# class NewsListView(TemplateView):
#     template_name = "real_estate/news_list.html"
class NewsListView(ListView):
    model = News
    template_name = 'real_estate/news_list.html'
    context_object_name = 'news'


class ContactsView(TemplateView):
    template_name = "real_estate/contacts.html"


class AboutView(TemplateView):
    template_name = "real_estate/about.html"


# class PropertyListView(TemplateView):
#     template_name = "real_estate/property_list.html"
class PropertyListView(ListView):
    model = RealEstate
    template_name = 'real_estate/property_list.html'
    context_object_name = 'properties'



