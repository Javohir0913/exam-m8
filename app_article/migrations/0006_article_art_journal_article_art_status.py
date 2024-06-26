# Generated by Django 5.0.6 on 2024-05-18 13:47

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_article', '0005_article_art_annotations_en_article_art_full_text_en_and_more'),
        ('app_journal', '0002_rename_journal_file_journal_journal_file'),
    ]

    operations = [
        migrations.AddField(
            model_name='article',
            name='art_journal',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='articles', to='app_journal.journal'),
        ),
        migrations.AddField(
            model_name='article',
            name='art_status',
            field=models.BooleanField(blank=True, null=True),
        ),
    ]
