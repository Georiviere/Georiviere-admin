# Generated by Django 3.1.14 on 2024-04-25 13:28

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('contribution', '0017_auto_20240423_1542'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='customcontribution',
            options={'ordering': ('-contributed_at',), 'verbose_name': 'Custom contribution', 'verbose_name_plural': 'Custom contributions'},
        ),
        migrations.AddField(
            model_name='customcontribution',
            name='contributed_at',
            field=models.DateTimeField(default=django.utils.timezone.now, verbose_name='Contributed at'),
        ),
    ]
