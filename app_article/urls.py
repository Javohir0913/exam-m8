from django.urls import path
from rest_framework import routers

from .views import (CategoryViewSet,
                    ReviewViewSet,
                    ArticleViewSet,
                    KeywordsViewSet,
                    article_post,
                    ArticleConfirmViewSet,
                    )


router = routers.DefaultRouter()
router.register('categories', CategoryViewSet)
router.register('reviews', ReviewViewSet)
router.register('articles', ArticleViewSet)
router.register('keywords', KeywordsViewSet)
router.register('article-confirm', ArticleConfirmViewSet, basename='article-confirm')

urlpatterns = [
    path('article-review/<int:obj_id>/', article_post, name='article-post'),
] + router.urls
