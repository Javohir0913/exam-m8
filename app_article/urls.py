from django.urls import path
from rest_framework import routers

from .views import CategoryViewSet, ReviewViewSet, ArticleViewSet, KeywordsViewSet, article_post


router = routers.DefaultRouter()
router.register('categories', CategoryViewSet)
router.register('reviews', ReviewViewSet)
router.register('articles', ArticleViewSet)
router.register('keywords', KeywordsViewSet)
urlpatterns = [
    path('article-review/<int:obj_id>', article_post, name='article-post'),
] + router.urls
