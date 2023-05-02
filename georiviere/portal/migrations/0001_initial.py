# Generated by Django 3.1.14 on 2023-04-19 12:01

import colorfield.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Portal',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_insert', models.DateTimeField(auto_now_add=True, verbose_name='Insertion date')),
                ('date_update', models.DateTimeField(auto_now=True, db_index=True, verbose_name='Update date')),
                ('name', models.CharField(help_text='Name of the portal', max_length=50, unique=True, verbose_name='Name')),
                ('website', models.URLField(max_length=256, unique=True, verbose_name='Website')),
                ('title', models.CharField(default='', help_text='Title on Georiviere', max_length=50, verbose_name='Title')),
                ('description', models.TextField(default='', help_text='Description on Georiviere', verbose_name='Description')),
                ('main_color', colorfield.fields.ColorField(default='#444444', help_text='Main color', max_length=18, verbose_name='Main color')),
            ],
            options={
                'verbose_name': 'Portal',
                'verbose_name_plural': 'Portals',
                'ordering': ('name',),
            },
        ),
    ]