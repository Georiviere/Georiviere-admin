# Generated by Django 3.1.14 on 2023-05-15 21:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('portal', '0003_auto_20230515_2019'),
        ('watershed', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='watershedtype',
            name='portals',
            field=models.ManyToManyField(blank=True, related_name='watersheds', to='portal.Portal', verbose_name='Published portals'),
        ),
    ]
