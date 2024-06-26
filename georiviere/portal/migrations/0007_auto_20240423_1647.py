# Generated by Django 3.1.14 on 2024-04-23 16:47

from django.db import migrations
from django.utils.translation import gettext_lazy as _


def add_station_map_layer_to_portals(apps, schema_editor):
    MapLayer = apps.get_model("portal", "MapLayer")
    Portal = apps.get_model("portal", "Portal")

    for portal in Portal.objects.all():
        MapLayer.objects.create(
            portal=portal,
            layer_type="stations",
            label=_("Stations"),
            hidden=True,
        )


class Migration(migrations.Migration):

    dependencies = [
        ("portal", "0006_auto_20230915_1756"),
    ]

    operations = [
        migrations.RunPython(
            add_station_map_layer_to_portals, reverse_code=migrations.RunPython.noop
        ),
    ]
