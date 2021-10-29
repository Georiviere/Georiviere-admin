# Generated by Django 3.1.6 on 2021-09-01 08:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('description', '0017_merge_20210608_1223'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='land',
            name='comment',
        ),
        migrations.AddField(
            model_name='land',
            name='description',
            field=models.TextField(blank=True, verbose_name='Description'),
        ),
        migrations.AddField(
            model_name='morphology',
            name='description',
            field=models.TextField(blank=True, verbose_name='Description'),
        ),
        migrations.AddField(
            model_name='status',
            name='description',
            field=models.TextField(blank=True, verbose_name='Description'),
        ),
        migrations.AddField(
            model_name='usage',
            name='description',
            field=models.TextField(blank=True, verbose_name='Description'),
        ),
    ]