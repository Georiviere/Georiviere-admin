# Generated by Django 3.1.14 on 2022-12-13 10:45

from django.db import migrations


def migrate_strata(apps, schema_editor):
    VegetationModel = apps.get_model('knowledge', 'Vegetation')
    vegetations_with_strata = VegetationModel.objects.filter(strata__isnull=False)
    for vegetation in vegetations_with_strata:
        vegetation.stratas.add(vegetation.strata)
        vegetation.save()


def reverse_migrate_strata(apps, schema_editor):
    VegetationModel = apps.get_model('knowledge', 'Vegetation')
    vegetations_with_stratas = VegetationModel.objects.filter(stratas__isnull=False)
    for vegetation in vegetations_with_stratas:
        vegetation.strata = vegetation.stratas.first()
        vegetation.save()


class Migration(migrations.Migration):

    dependencies = [
        ('knowledge', '0013_vegetation_stratas'),
    ]

    operations = [
        migrations.RunPython(migrate_strata, reverse_migrate_strata)
    ]