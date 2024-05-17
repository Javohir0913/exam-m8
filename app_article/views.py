from time import time

from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from django_filters.rest_framework import DjangoFilterBackend


from users.permissions import IsSuperUser, IsAuthenticatedOrGet
from .filters import ArticleFilter
from .serializers import (
    CategorySerializer,
    ReviewSerializer,
    ArticleListSerializer,
    ArticlePostSerializer,
    ArticleSerializer,
    ArticlePostReviewSerializer,
    KeywordsSerializer
)
from .models import Category, Review, Article, Keywords


# Create your views here.
class KeywordsViewSet(ModelViewSet):
    queryset = Keywords.objects.all()
    serializer_class = KeywordsSerializer
    permission_classes = (IsSuperUser,)

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)
        return serializer.save


class CategoryViewSet(ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsSuperUser]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)
        return serializer.save


class ReviewViewSet(ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [IsSuperUser]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)
        return serializer.save

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.status = False
        instance.save()
        return Response({'message': "success delete"}, status=status.HTTP_204_NO_CONTENT)


class ArticleViewSet(ModelViewSet):
    queryset = Article.objects.all()
    serializer_class = ArticleListSerializer
    permission_classes = [IsAuthenticatedOrGet]
    pagination_class = PageNumberPagination
    pagination_class.page_size = 6
    filter_backends = [DjangoFilterBackend]
    filterset_class = ArticleFilter

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)
        return serializer.save
    
    def retrieve(self, request, pk=None, *args, **kwargs):
        print()
        user = f"atr_{request.user.id}_{pk}"
        if user in request.COOKIES:
            if time() - float(request.COOKIES[user]) > 3600:
                up = True
            else:
                up = False
        else:
            up = True
        if up:
            article = Article.objects.get(pk=pk).art_views
            Article.objects.filter(pk=pk).update(art_views=article + 1)
        res = super().retrieve(request, *args, **kwargs)
        res.set_cookie(user, time())
        return res

    def get_serializer_class(self):
        if self.action == 'list':
            return ArticleListSerializer
        elif self.action == 'create':
            return ArticlePostSerializer
        return ArticleSerializer


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def article_post(request, obj_id):
    serializer = ArticlePostReviewSerializer(data=request.data)
    if serializer.is_valid():
        obj = Review.objects.create(author=request.user, file=request.data.get('file'))
        obj.save()
        art = Article.objects.get(id=obj_id).art_reviews
        art.add(obj.id)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
