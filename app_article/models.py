from django.db import models

from ckeditor.fields import RichTextField
from django.contrib.auth import get_user_model


# Create your models here.
class Keywords(models.Model):
    keywords = models.CharField(max_length=255)
    author = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)

    def __str__(self):
        return str(self.keywords)

    class Meta:
        verbose_name_plural = 'Keywords'
        verbose_name = 'Keyword'
        db_table = 'keywords'


class Category(models.Model):
    cat_name = models.CharField(max_length=255, unique=True)
    cat_datetime = models.DateTimeField(auto_now=True)
    author = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)

    def __str__(self):
        return str(self.cat_name)

    class Meta:
        verbose_name_plural = 'Categories'
        verbose_name = 'Category'
        db_table = 'category'


class Review(models.Model):
    author = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    file = models.FileField(upload_to='reviews/')
    status = models.BooleanField(default=True)
    datetime = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"'{self.author}' ({self.id})"

    class Meta:
        verbose_name_plural = 'Reviews'
        verbose_name = 'Review'
        db_table = 'review'


class Article(models.Model):
    art_category = models.ManyToManyField(Category, related_name='articles', blank=True)
    art_title = models.CharField(max_length=255)
    art_datetime = models.DateTimeField(auto_now=True)
    art_views = models.IntegerField(default=0)
    author = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    art_annotations = models.CharField(max_length=255)
    art_full_text = RichTextField()
    art_references = RichTextField()
    art_count_reviews = models.IntegerField(default=0)
    art_reviews = models.ManyToManyField(Review, related_name='articles', blank=True)
    art_keywords = models.ManyToManyField(Keywords, related_name='articles', blank=True)

    def __str__(self):
        return str(self.art_title)

    class Meta:
        verbose_name_plural = 'Articles'
        verbose_name = 'Article'
        db_table = 'article'
        ordering = ('-art_views', 'art_datetime')
