# Generated by Django 3.1.14 on 2022-12-13 11:30

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('description', '0022_auto_20221213_1104'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='morphology',
            name='secondary_flow',
        ),
        migrations.RemoveField(
            model_name='morphology',
            name='secondary_habitat',
        ),
    ]
