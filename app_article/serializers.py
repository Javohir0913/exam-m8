from rest_framework import serializers

from .models import Category, Review, Article, Keywords


class KeywordsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Keywords
        fields = ('id', 'keywords')


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('id', 'cat_name',)


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ('id', 'file',)


class ReviewArtSerializer(serializers.ModelSerializer):
    author = serializers.SerializerMethodField(method_name='get_author', read_only=True, source='author')

    class Meta:
        model = Review
        fields = ('id', 'file', 'author')

    def get_author(self, obj):
        return obj.author.username


# -------------- Article  ------------------
class ArticleListSerializer(serializers.ModelSerializer):
    detail = serializers.SerializerMethodField(method_name='get_detail', read_only=True, source='detail')
    author = serializers.SerializerMethodField(method_name='get_author', read_only=True, source='author')
    art_category = CategorySerializer(many=True, read_only=True)
    class Meta:
        model = Article
        fields = ('id', 'art_category', 'art_title', 'author', 'art_datetime', 'art_views', 'art_annotations', 'detail')

    def get_detail(self, obj):
        return f"http://localhost:8000/api/articles/{obj.id}/"

    def get_author(self, obj):
        return obj.author.username


class ArticleSerializer(serializers.ModelSerializer):
    art_category = CategorySerializer(many=True, read_only=True)
    art_keywords = KeywordsSerializer(many=True, read_only=True)
    art_reviews = ReviewArtSerializer(many=True, read_only=True)
    author = serializers.SerializerMethodField(method_name='get_author', read_only=True, source='author')

    class Meta:
        model = Article
        fields = '__all__'

    def get_author(self, obj):
        return obj.author.username


class ArticlePostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Article
        fields = ('id', 'art_title', 'art_annotations', 'art_category',
                  'art_full_text', 'art_references', 'art_keywords')
        extra_kwargs = {
            'art_keywords': {'required': True},
            'art_category': {'required': True},
            'art_references': {'required': False},
        }


class ArticlePostReviewSerializer(serializers.Serializer):
    file = serializers.FileField(required=True)
