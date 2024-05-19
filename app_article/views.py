from time import time

from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated, IsAdminUser
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
    ArticlePostReviewSerializer,
    KeywordsSerializer, ArticleDetailSerializer
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
    permission_classes = [IsAdminUser]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)
        return serializer.save


class ReviewViewSet(ModelViewSet):
    queryset = Review.objects.filter(status=True)
    serializer_class = ReviewSerializer
    permission_classes = [IsSuperUser]
    http_method_names = ['get', 'delete']

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

    def get_serializer_class(self):
        if self.action == 'list':
            return ArticleListSerializer
        elif self.action == 'create':
            return ArticlePostSerializer
        elif self.action == 'retrieve':
            return ArticleDetailSerializer
        return ArticleDetailSerializer

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset().filter(art_is_delete=False))
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None, *args, **kwargs):
        instance = self.get_object()
        if instance.art_is_delete is True:
            return Response({'message': "article has been deleted"}, status=status.HTTP_204_NO_CONTENT)
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

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.art_is_delete = True
        instance.save()
        return Response({'message': "success delete"}, status=status.HTTP_204_NO_CONTENT)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def article_post(request, obj_id):
    serializer = ArticlePostReviewSerializer(data=request.data)
    if serializer.is_valid():
        obj = Review.objects.create(author=request.user, file=request.data.get('file'))
        obj.save()
        art = Article.objects.get(id=obj_id).art_reviews
        art.add(obj.id)
        return Response({'message': 'Review success add'}, status=status.HTTP_201_CREATED)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ArticleConfirmViewSet(ModelViewSet):
    queryset = Article.objects.filter(art_status=None)
    serializer_class = ArticleDetailSerializer
    permission_classes = [IsAdminUser]
    http_method_names = ['get', 'put', 'patch']
    pagination_class = PageNumberPagination
    pagination_class.page_size = 6

    def create(self, request, *args, **kwargs):
        response = {'message': 'Create function is not offered in this path.'}
        return Response(response, status=status.HTTP_403_FORBIDDEN)

    def destroy(self, request, pk=None, *args, **kwargs):
        response = {'message': 'Delete function is not offered in this path.'}
        return Response(response, status=status.HTTP_403_FORBIDDEN)
