# Generated by Django 3.1.14 on 2024-05-14 08:49

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('observations', '0023_auto_20230220_1703'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='station',
            options={'ordering': ('label', 'pk'), 'verbose_name': 'Station', 'verbose_name_plural': 'Stations'},
        ),
    ]
