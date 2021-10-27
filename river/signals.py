from django.db.models.signals import post_save
from django.db.models.fields.reverse_related import OneToOneRel
from django.dispatch import receiver

from river.models import Stream, Topology


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
