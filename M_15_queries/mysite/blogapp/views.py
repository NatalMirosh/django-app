from django.shortcuts import render
from django.views.generic import ListView

from blogapp.models import Article
import logging


# class ArticleListView(ListView):
#     template_name = 'article_list.html'
#     context_object_name = 'articles'
#     queryset = Article.objects.select_related('author', 'category').prefetch_related('tags')


logger = logging.getLogger(__name__)


class ArticleListView(ListView):
    model = Article
    template_name = 'article_list.html'
    context_object_name = 'articles'

    def get_queryset(self):
        queryset = super().get_queryset().select_related('author', 'category')
        queryset = queryset.prefetch_related('tags')
        queryset = queryset.defer('content')

        logger.info('Start blog list')
        return queryset
