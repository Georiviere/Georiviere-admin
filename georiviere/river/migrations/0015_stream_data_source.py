# Generated by Django 3.1.14 on 2022-03-23 16:56

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0008_datasource'),
        ('river', '0014_stream_flow'),
    ]

    operations = [
        migrations.AddField(
            model_name='stream',
            name='data_source',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='rivers', to='main.datasource', verbose_name='Data source'),
        ),
    ]
