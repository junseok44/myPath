# Generated by Django 4.2.4 on 2023-08-15 05:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0007_alter_user_kakaoid'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='googleId',
            field=models.CharField(blank=True, max_length=30, null=True),
        ),
        migrations.AddField(
            model_name='user',
            name='naverId',
            field=models.CharField(blank=True, max_length=30, null=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='kakaoId',
            field=models.CharField(blank=True, max_length=30, null=True),
        ),
    ]
