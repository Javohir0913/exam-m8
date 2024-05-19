from django.contrib import admin
from .models import Category, Review, Article, Keywords


class ArticleAdmin(admin.ModelAdmin):
    list_filter = ('art_title_uz', 'author')
    search_fields = ('art_title_uz', 'author')
    list_per_page = 10


admin.site.register(Article, ArticleAdmin)
admin.site.register(Keywords)
admin.site.register(Category)
admin.site.register(Review)



