# Generated by Django 4.2.4 on 2023-09-10 14:48

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('post', '0004_push_text'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='push',
            name='path',
        ),
        migrations.AddField(
            model_name='push',
            name='post',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='push_post', to='post.post'),
        ),
    ]
