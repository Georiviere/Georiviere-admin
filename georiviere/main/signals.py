from django.contrib.gis.db.models.functions import Distance, Length, LineLocatePoint
from django.contrib.contenttypes.models import ContentType
from django.db.models import F, FloatField, Case, When

from georiviere.functions import ClosestPoint, LineSubString
from georiviere.river.models import Stream
from georiviere.main.models import DistanceToSource


def annotate_distance_to_source(streams, instance):
    if streams:
        streams = streams.annotate(
            locate_source=LineLocatePoint(F('geom'), F('source_location')),
            locate_object=LineLocatePoint(F('geom'), ClosestPoint(F('geom'), instance.geom)),
            locate=Length(LineSubString(F('geom'),
                                        Case(
                                            When(locate_source__gte=F('locate_object'), then=F('locate_object')),
                                            default=F('locate_source')),
                                        Case(
                                            When(locate_source__gte=F('locate_object'), then=F('locate_source')),
                                            default=F('locate_object')))) + Distance(
                instance.geom,
                F('geom'),
                output_field=FloatField()) + Distance(
                F('geom'),
                F('source_location'),
                output_field=FloatField())
        )
    return streams


def save_objects_generate_distance_to_source(sender, instance, **kwargs):
    if not hasattr(instance, 'get_topology'):
        streams = annotate_distance_to_source(instance.streams, instance)
        for stream in streams:
            DistanceToSource.objects.update_or_create(
                object_id=instance.pk,
                content_type=ContentType.objects.get_for_model(instance._meta.model),
                stream=stream,
                defaults={"distance": stream.locate.m}
            )
        if not kwargs.get('created'):
            DistanceToSource.objects.filter(object_id=instance.pk,
                                            content_type=ContentType.objects.get_for_model(instance._meta.model),
                                            ).exclude(stream__in=streams).delete()

    elif hasattr(instance, 'topology'):
        stream = annotate_distance_to_source(Stream.objects.all(), instance).get(pk=instance.topology.stream.pk)
        DistanceToSource.objects.update_or_create(
            object_id=instance.pk,
            content_type=ContentType.objects.get_for_model(instance._meta.model),
            stream=stream,
            defaults={"distance": stream.locate.m}
        )


def delete_objects_remove_distance_to_source(sender, instance, **kwargs):
    content_type = ContentType.objects.get_for_model(instance._meta.model)
    DistanceToSource.objects.filter(content_type=content_type, object_id=instance.pk).delete()
