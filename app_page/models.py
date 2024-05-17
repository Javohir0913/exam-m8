from django.contrib.auth import get_user_model
from django.db import models
from ckeditor.fields import RichTextField


# Create your models here.
class FAQ(models.Model):
    question = models.TextField()
    answer = models.TextField()
    author = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)

    def __str__(self):
        return self.question

    class Meta:
        verbose_name = 'FAQ'
        verbose_name_plural = 'FAQs'
        db_table = 'FAQ'


class Contacts(models.Model):
    address = models.TextField()
    telephone = models.TextField()
    email = models.EmailField()

    def __str__(self):
        return self.address

    class Meta:
        verbose_name = 'Info'
        verbose_name_plural = 'Infos'
        db_table = 'info'
        ordering = ['-id']


class Requirements(models.Model):
    requirements = models.TextField()
    full_text = RichTextField()
    author = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)

    def __str__(self):
        return self.requirements

    class Meta:
        verbose_name = 'Requirements'
        verbose_name_plural = 'Requirements'
        db_table = 'requirements'


class Appeal(models.Model):
    first_name = models.CharField(max_length=255)
    email = models.EmailField()
    message = models.TextField()
