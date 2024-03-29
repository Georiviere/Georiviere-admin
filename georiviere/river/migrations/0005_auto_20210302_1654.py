# Generated by Django 3.1.7 on 2021-03-02 16:54

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('river', '0004_auto_20210209_1534'),
    ]

    operations = [
        migrations.AddField(
            model_name='stream',
            name='date_insert',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now, verbose_name='Insertion date'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='stream',
            name='date_update',
            field=models.DateTimeField(auto_now=True, db_index=True, verbose_name='Update date'),
        ),
    ]
