# Generated by Django 3.1.14 on 2023-07-25 12:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contribution', '0005_contribution_validated'),
    ]

    operations = [
        migrations.AddField(
            model_name='contribution',
            name='publication_date',
            field=models.DateField(blank=True, editable=False, null=True, verbose_name='Publication date'),
        ),
    ]
