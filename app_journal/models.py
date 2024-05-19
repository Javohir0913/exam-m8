from django.contrib.auth import get_user_model
from django.db import models


# Create your models here.
class Tags(models.Model):
    tag_name = models.CharField(max_length=255)
    author = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    tag_datetime = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.tag_name)

    class Meta:
        verbose_name_plural = "Tags"
        verbose_name = "Tag"
        db_table = "tags"


class Journal(models.Model):
    jornal_name = models.CharField(max_length=255)
    journal_description = models.CharField(max_length=255)
    jornal_logo = models.FileField(upload_to="journal_logo/%Y/%m/%d")
    journal_file = models.FileField(upload_to="journal_files/%Y/%m/%d")
    jornal_tags = models.ManyToManyField(Tags, blank=True)
    jornal_author = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    jornal_datetime = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.jornal_name)

    class Meta:
        verbose_name_plural = "Journal"
        verbose_name = "Journal"
        db_table = "journal"

