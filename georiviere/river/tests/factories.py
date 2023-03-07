import factory
from geotrek.authent.tests.factories import StructureFactory

from georiviere.tests.factories import BaseLineStringFactory
from georiviere.river.models import ClassificationWaterPolicy, Stream, Topology


class ClassificationWaterPolicyFactory(factory.django.DjangoModelFactory):
    label = factory.Sequence(lambda n: "Classification water policy %s" % n)

    class Meta:
        model = ClassificationWaterPolicy


class WithStreamFactory(factory.django.DjangoModelFactory):
    @factory.post_generation
    def with_stream(obj, create, with_stream):
        if not create or not with_stream:
            return
        if with_stream and obj.geom:
            # Status / Morphology is already on a stream
            # It should not add this next stream in distance to source
            StreamFactory.create(geom_around=obj.geom)


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
