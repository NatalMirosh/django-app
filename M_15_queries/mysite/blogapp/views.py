from django.shortcuts import render
from django.views.generic import ListView

from blogapp.models import Article


# class ArticleListView(ListView):
#     template_name = 'article_list.html'
#     context_object_name = 'articles'
#     queryset = Article.objects.select_related('author', 'category').prefetch_related('tags')

class ArticleListView(ListView):
    model = Article
    template_name = 'article_list.html'
    context_object_name = 'articles'

    def get_queryset(self):
        queryset = super().get_queryset().select_related('author', 'category')
        queryset = queryset.prefetch_related('tags')
        queryset = queryset.defer('content')

        return queryset
