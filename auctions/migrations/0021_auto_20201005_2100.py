# Generated by Django 3.1 on 2020-10-05 20:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0020_closedlisting_title'),
    ]

    operations = [
        migrations.AlterField(
            model_name='closedlisting',
            name='winner',
            field=models.CharField(blank=True, max_length=64, null=True),
        ),
    ]