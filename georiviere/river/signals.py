from django.apps import apps
from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from django.contrib.gis.db.models.functions import Distance, Length, LineLocatePoint
from django.db.models.signals import post_save
from django.db.models.fields.reverse_related import OneToOneRel
from django.db.models import F, FloatField, Case, When
from django.dispatch import receiver

from georiviere.functions import ClosestPoint, LineSubString
from georiviere.main.models import DistanceToSource
from georiviere.river.models import Stream, Topology, TopologyMixin

from mapentity.models import MapEntityMixin


@receiver(post_save, sender=Stream)
def save_stream(sender, instance, **kwargs):
    if kwargs['created']:
        class_topos = [field.related_model for field in instance.topologies.model._meta.get_fields()
                       if isinstance(field, OneToOneRel)]
        for class_topo in class_topos:
            topology = Topology.objects.create(start_position=0, end_position=1, stream=instance)
            class_topo.objects.create(topology=topology, geom=instance.geom)
    else:
        for topology in instance.topologies.all():
            topology.save()


@receiver(post_save, sender=Stream)
def save_stream_generate_distance_to_source(sender, instance, **kwargs):

    for model in apps.get_models():
        if issubclass(model, MapEntityMixin) and not issubclass(model, TopologyMixin) and model != Stream and 'geom' in [field.name for field in model._meta.get_fields()]:
            distances_to_sources = []
            area = instance.geom.buffer(settings.BASE_INTERSECTION_MARGIN)
            for object_topology in model.objects.annotate(
                locate_source=LineLocatePoint(instance.geom,
                                              instance.source_location),
                locate_object=LineLocatePoint(instance.geom,
                                              ClosestPoint(instance.geom,
                                                           F('geom'))),
                locate=Length(LineSubString(instance.geom,
                                            Case(
                                                When(locate_source__gte=F('locate_object'), then=F('locate_object')),
                                                default=F('locate_source')
                                            ),
                                            Case(
                                                When(locate_source__gte=F('locate_object'), then=F('locate_source')),
                                                default=F('locate_object')
                                            ))) + Distance(F('geom'),
                                                           instance.geom,
                                                           output_field=FloatField()) + Distance(instance.geom,
                                                                                                 instance.source_location,
                                                                                                 output_field=FloatField())
            ).filter(geom__intersects=area):
                distances_to_sources.append(DistanceToSource.objects.update_or_create(
                    object_id=object_topology.pk,
                    content_type=ContentType.objects.get_for_model(object_topology._meta.model),
                    stream=instance,
                    defaults={"distance": object_topology.locate}
                )[0].pk)
            if not kwargs['created']:
                DistanceToSource.objects.exclude(pk__in=distances_to_sources).filter(stream=instance.pk, content_type=ContentType.objects.get_for_model(model)).delete()
