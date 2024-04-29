# Generated by Django 3.1.14 on 2024-04-29 07:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contribution', '0019_auto_20240426_1532'),
    ]

    operations = [
        migrations.AddField(
            model_name='customcontributiontype',
            name='password',
            field=models.CharField(blank=True, default='', help_text='Define if password is required to send the form', max_length=128, verbose_name='Password'),
        ),
    ]