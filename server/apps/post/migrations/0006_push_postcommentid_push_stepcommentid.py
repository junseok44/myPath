# Generated by Django 4.2.4 on 2023-09-14 15:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('post', '0005_remove_push_path_push_post'),
    ]

    operations = [
        migrations.AddField(
            model_name='push',
            name='postCommentId',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='push',
            name='stepCommentId',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
