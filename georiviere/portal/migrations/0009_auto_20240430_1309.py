# Generated by Django 3.1.14 on 2024-04-30 13:09

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('portal', '0008_auto_20240429_1233'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='mapbaselayer',
            options={'ordering': ('order',), 'verbose_name': 'Map base layer', 'verbose_name_plural': 'Map base layers'},
        ),
    ]