# Generated by Django 3.1.2 on 2021-07-04 00:56

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0006_auto_20210703_1952'),
    ]

    operations = [
        migrations.RenameField(
            model_name='listing',
            old_name='creation_at',
            new_name='created_at',
        ),
    ]
