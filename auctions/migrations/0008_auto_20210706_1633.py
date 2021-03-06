# Generated by Django 3.1.2 on 2021-07-06 21:33

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0007_auto_20210703_1956'),
    ]

    operations = [
        migrations.AddField(
            model_name='listing',
            name='followers',
            field=models.ManyToManyField(blank=True, related_name='watchlist', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='listing',
            name='desc',
            field=models.CharField(blank=True, max_length=500),
        ),
        migrations.AlterField(
            model_name='listing',
            name='url',
            field=models.CharField(blank=True, max_length=128),
        ),
    ]
