# Generated by Django 3.1 on 2020-10-06 21:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0023_auto_20201006_2247'),
    ]

    operations = [
        migrations.AlterField(
            model_name='listing',
            name='url',
            field=models.URLField(blank=True, null=True),
        ),
    ]
