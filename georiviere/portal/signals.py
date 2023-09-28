from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver

from django.utils.translation import gettext_lazy as _

from georiviere.portal.models import MapBaseLayer, MapLayer, Portal
from georiviere.valorization.models import POICategory


@receiver(post_delete, sender=POICategory, dispatch_uid='delete_category_maplayer')
def delete_category_maplayer(sender, instance, **kwargs):
    # Remove every map layer (all portals) when a category is deleted
    MapLayer.objects.filter(layer_type__startswith='pois',
                            layer_type__endswith=instance.pk).delete()


@receiver(post_save, sender=POICategory, dispatch_uid='save_category')
def save_category_maplayer(sender, instance, created, **kwargs):
    if created:
        for portal in Portal.objects.all():
            # Create a map layer for each portal for this POICategory
            MapLayer.objects.create(label=instance.label, order=0, layer_type=f'pois-{instance.pk}',
                                    portal=portal)


@receiver(post_save, sender=Portal, dispatch_uid='save_portal')
def save_portal(sender, instance, created, **kwargs):
    if created:
        # Generate a default base layer
        MapBaseLayer.objects.create(label='OSM', order=0, url='https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png',
                                    attribution='© Contributeurs OpenStreetMap', portal=instance)
        # Generate all layers
        MapLayer.objects.create(label=_('Watershed'), order=0, layer_type=_('watersheds'), portal=instance)
        MapLayer.objects.create(label=_('City'), order=0, layer_type=_('cities'), portal=instance)
        MapLayer.objects.create(label=_('Sensitivity'), order=0, layer_type=_('sensitivities'), portal=instance)
        MapLayer.objects.create(label=_('District'), order=0, layer_type=_('districts'), portal=instance)
        MapLayer.objects.create(label=_('Contribution'), order=0, layer_type=_('contributions'), portal=instance)
        # We generate a map layer for each category of poi with the layer type separated by a -
        # We use it after in the serializer / view to generate a geojson url for each of them
        for category in POICategory.objects.all():
            MapLayer.objects.create(label=f'{category.label}', order=0, layer_type=f'pois-{category.pk}',
                                    portal=instance)

        MapLayer.objects.create(label=_('Stream'), order=0, layer_type=_('streams'), portal=instance)
