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
        fields = ('id', 'file', 'author', 'status')

    def get_author(self, obj):
        return obj.author.username


# -------------- Article  ------------------
class ArticleListSerializer(serializers.ModelSerializer):
    detail = serializers.SerializerMethodField(method_name='get_detail', read_only=True, source='detail')
    author = serializers.SerializerMethodField(method_name='get_author', read_only=True, source='author')
    art_category = CategorySerializer(many=True, read_only=True)
    art_title = serializers.SerializerMethodField(method_name='get_art_title', read_only=True, source='title')
    art_annotations = serializers.SerializerMethodField(
        method_name='get_art_annotations', read_only=True, source='annotations')

    class Meta:
        model = Article
        fields = ('id', 'art_category', 'art_title', 'author', 'art_datetime', 'art_views', 'art_annotations', 'detail')

    def get_detail(self, obj):
        return f"http://localhost:8000/api/articles/{obj.id}/"

    def get_author(self, obj):
        return obj.author.username

    def get_art_title(self, obj):
        try:
            lang = self.context['request'].GET['lang']
            if lang == 'en':
                return obj.art_title_en
            return obj.art_title_uz
        except:
            return obj.art_title_uz

    def get_art_annotations(self, obj):
        try:
            lang = self.context['request'].GET['lang']
            if lang == 'en':
                return obj.art_annotations_en
            return obj.art_annotations_uz
        except:
            return obj.art_annotations_uz


class ArticleDetailSerializer(serializers.ModelSerializer):
    art_category = CategorySerializer(many=True)
    art_keywords = KeywordsSerializer(many=True)
    art_reviews = ReviewArtSerializer(many=True, read_only=True)
    author = serializers.SerializerMethodField(method_name='get_author', read_only=True, source='author')
    art_title = serializers.SerializerMethodField(method_name='get_art_title', read_only=True, source='title')

    art_annotations = serializers.SerializerMethodField(
        method_name='get_art_annotations', read_only=True, source='annotations')

    art_full_text = serializers.SerializerMethodField(
        method_name='get_art_full_text', read_only=True, source='full_text')

    class Meta:
        model = Article
        fields = '__all__'
        extra_kwargs = {
            'art_title_uz': {'write_only': True},
            'art_title_en': {'write_only': True},
            'art_annotations_uz': {'write_only': True},
            'art_annotations_en': {'write_only': True},
            'art_full_text_uz': {'write_only': True},
            'art_full_text_en': {'write_only': True},
        }

    def get_author(self, obj):
        return obj.author.username

    def get_art_title(self, obj):
        try:
            lang = self.context['request'].GET['lang']
            print(lang)
            if lang == 'en':
                return obj.art_title_en
            return obj.art_title_uz
        except:
            return obj.art_title_uz

    def get_art_annotations(self, obj):
        try:
            lang = self.context['request'].GET['lang']
            if lang == 'en':
                return obj.art_annotations_en
            return obj.art_annotations_uz
        except:
            return obj.art_annotations_uz

    def get_art_full_text(self, obj):
        try:
            lang = self.context['request'].GET['lang']
            if lang == 'en':
                return obj.art_full_text_en
            return obj.art_full_text_uz
        except:
            return obj.art_full_text_uz


class ArticlePostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Article
        fields = ('id', 'art_title_uz', 'art_title_en', 'art_annotations_uz', 'art_annotations_en', 'art_category',
                  'art_full_text_uz', 'art_full_text_en', 'art_references', 'art_keywords', 'art_journal')
        extra_kwargs = {
            'art_keywords': {'required': True},
            'art_category': {'required': True},
            'art_references': {'required': False},
        }


class ArticlePostReviewSerializer(serializers.Serializer):
    file = serializers.FileField(required=True)


# ------------------- ORDER BY------------------


class ArticleOrderBySerializer(serializers.ModelSerializer):
    art_title = serializers.SerializerMethodField(method_name='get_art_title')
    art_annotations = serializers.SerializerMethodField(method_name='get_art_annotations')

    class Meta:
        model = Article
        fields = ('id', 'art_title', 'art_annotations')

    def get_art_title(self, obj):
        try:
            lang = self.context['request'].GET['lang']
            if lang == 'en':
                return obj.art_title_en
            return obj.art_title_uz
        except:
            return obj.art_title_uz

    def get_art_annotations(self, obj):
        try:
            lang = self.context['request'].GET['lang']
            if lang == 'en':
                return obj.art_annotations_en
            return obj.art_annotations_uz
        except:
            return obj.art_annotations_uz
