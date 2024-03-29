# Generated by Django 3.1.14 on 2023-03-27 08:14

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('authent', '0005_remove_userprofile_language'),
        ('main', '0009_auto_20230223_1541'),
        ('river', '0016_auto_20220324_1419'),
    ]

    operations = [
        migrations.AlterField(
            model_name='stream',
            name='data_source',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='streams', to='main.datasource', verbose_name='Data source'),
        ),
        migrations.CreateModel(
            name='ClassificationWaterPolicy',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('label', models.CharField(max_length=128, verbose_name='Label')),
                ('structure', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='authent.structure', verbose_name='Related structure')),
            ],
            options={
                'verbose_name': 'Classification water policy',
                'verbose_name_plural': 'Classification water policies',
            },
        ),
        migrations.AddField(
            model_name='stream',
            name='classification_water_policy',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='streams', to='river.classificationwaterpolicy', verbose_name='Classification water policy'),
        ),
    ]
