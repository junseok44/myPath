# Generated by Django 4.2.4 on 2023-09-22 06:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0011_remove_usercard_profile_user_profile'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='profile',
            field=models.ImageField(blank=True, default='static/resource/noimage.jpg', null=True, upload_to='user/'),
        ),
    ]
