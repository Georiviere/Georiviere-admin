# Generated by Django 3.1.6 on 2021-02-02 14:02

from django.conf import settings
import django.contrib.gis.db.models.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0003_auto_20210201_1849'),
    ]

    operations = [
        migrations.AlterField(
            model_name='network',
            name='geom',
            field=django.contrib.gis.db.models.fields.LineStringField(srid=settings.SRID),
        ),
    ]