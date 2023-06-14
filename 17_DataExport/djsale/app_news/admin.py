from django.contrib import admin
from app_news.models import NewsItem, NewsType


class NewsItemAdmin(admin.ModelAdmin):
    list_display = ['id', 'title']


class NewsTypeAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'code']


admin.site.register(NewsItem, NewsItemAdmin)
admin.site.register(NewsType, NewsTypeAdmin)