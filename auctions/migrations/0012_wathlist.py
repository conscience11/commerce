# Generated by Django 3.1 on 2020-10-04 15:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0011_auto_20201004_1128'),
    ]

    operations = [
        migrations.CreateModel(
            name='Wathlist',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('owner', models.CharField(max_length=64)),
                ('listid', models.IntegerField()),
            ],
        ),
    ]
