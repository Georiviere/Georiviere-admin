from django.db import migrations


def generate_topologies_every_stream(apps, schema_editor):
    TopologyModel = apps.get_model('river', 'Topology')
    StreamModel = apps.get_model('river', 'Stream')
    MorphologyModel = apps.get_model('description', 'Morphology')
    StatusModel = apps.get_model('description', 'Status')
    for stream in StreamModel.objects.all():
        if not TopologyModel.objects.filter(stream=stream).exists():
            topo_morpho = TopologyModel.objects.create(start_position=0, end_position=1, stream=stream)
            MorphologyModel.objects.create(topology=topo_morpho, geom=stream.geom)
            topo_status = TopologyModel.objects.create(start_position=0, end_position=1, stream=stream)
            StatusModel.objects.create(topology=topo_status, geom=stream.geom)


class Migration(migrations.Migration):

    dependencies = [
        ('description', '0013_auto_20210413_1327'),
    ]

    operations = [
        migrations.RunPython(generate_topologies_every_stream)
    ]
