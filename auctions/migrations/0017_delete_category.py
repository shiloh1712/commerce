# Generated by Django 3.1.2 on 2021-07-13 01:52

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0016_category'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Category',
        ),
    ]