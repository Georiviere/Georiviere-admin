import factory
from geotrek.authent.tests.factories import StructureFactory

from georiviere.tests.factories import BaseLineStringFactory
from georiviere.river.models import ClassificationWaterPolicy, Stream, Topology


class ClassificationWaterPolicyFactory(factory.django.DjangoModelFactory):
    label = factory.Sequence(lambda n: "Classification water policy %s" % n)

    class Meta:
        model = ClassificationWaterPolicy


class StreamFactory(BaseLineStringFactory):
    name = factory.Sequence(lambda n: 'stream-%d' % n)
    structure = factory.SubFactory(StructureFactory)
    classification_water_policy = factory.SubFactory(ClassificationWaterPolicyFactory)

    class Meta:
        model = Stream


class TopologyFactory(factory.django.DjangoModelFactory):
    stream = factory.SubFactory(StreamFactory)
    start_position = 0.1
    end_position = 0.9
    qualified = False

    class Meta:
        model = Topology
