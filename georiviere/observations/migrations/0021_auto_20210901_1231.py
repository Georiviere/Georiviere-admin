# Generated by Django 3.1.6 on 2021-09-01 12:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('observations', '0020_auto_20210831_1429'),
    ]

    operations = [
        migrations.AlterField(
            model_name='station',
            name='in_service',
            field=models.BooleanField(blank=True, null=True, verbose_name='In service'),
        ),
    ]
