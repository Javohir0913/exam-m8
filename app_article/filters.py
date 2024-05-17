import django_filters
from django.contrib.auth import get_user_model

from .models import Article, Keywords


class ArticleFilter(django_filters.FilterSet):
    title = django_filters.CharFilter(lookup_expr='icontains', label='Title', field_name='art_title')
    author = django_filters.CharFilter(label='Author', method='filter_author')
    art_keyword = django_filters.CharFilter(label='Keywords', method='filter_keywords')
    references = django_filters.CharFilter(label='References', lookup_expr='icontains', field_name='art_reference')
    art_category = django_filters.CharFilter(label='Category', method='filter_category')

    class Meta:
        model = Article
        fields = ['author', 'art_keyword', 'art_category']

    def filter_author(self, queryset, name, value):
        if not value:
            return queryset
        try:
            return queryset.filter(author__username=value)
        except:
            return queryset

    def filter_keywords(self, queryset, name, value):
        if not value:
            return queryset
        try:
            return queryset.filter(art_keywords__keywords=value)
        except:
            return queryset

    def filter_category(self, queryset, name, value):
        if not value:
            return queryset
        try:
            return queryset.filter(art_category__cat_name=value)
        except:
            return queryset
