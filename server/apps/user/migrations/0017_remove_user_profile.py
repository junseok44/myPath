# Generated by Django 4.2.4 on 2023-09-22 12:24

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0016_alter_user_profile'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='profile',
        ),
    ]
