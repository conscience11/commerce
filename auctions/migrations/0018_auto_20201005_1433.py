# Generated by Django 3.1 on 2020-10-05 13:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0017_auto_20201005_1322'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bid',
            name='bid',
            field=models.CharField(max_length=5000000000000000),
        ),
    ]
