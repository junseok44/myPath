# Generated by Django 4.2.4 on 2023-09-18 05:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0009_usercard'),
    ]

    operations = [
        migrations.AddField(
            model_name='usercard',
            name='profile',
            field=models.ImageField(blank=True, null=True, upload_to='user/'),
        ),
    ]
