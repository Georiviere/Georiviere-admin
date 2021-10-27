from django.db import migrations


def remove_topologies_morphology(apps, schema_editor):
    MorphologyModel = apps.get_model('description', 'Morphology')
    StatusModel = apps.get_model('description', 'Status')
    MorphologyModel.objects.all().delete()
    StatusModel.objects.all().delete()


class Migration(migrations.Migration):

    dependencies = [
        ('description', '0011_auto_20210330_1534'),
    ]

    operations = [
        migrations.RunPython(remove_topologies_morphology)
    ]
