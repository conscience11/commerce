# Generated by Django 3.1 on 2020-10-06 22:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0024_auto_20201006_2250'),
    ]

    operations = [
        migrations.AlterField(
            model_name='listing',
            name='url',
            field=models.URLField(default='https://i.dlpng.com/static/png/5399245-avengers-endgame-2019-avengers-logo-png-by-mintmovi3-on-deviantart-avengers-logo-png-859_930_preview.png'),
        ),
    ]