from factory import django, Sequence, SubFactory, post_generation

from georiviere.description.tests.factories import LandFactory
from georiviere.maintenance import models
from georiviere.river.tests.factories import StreamFactory, WithStreamFactory


class InterventionStatusFactory(django.DjangoModelFactory):
    class Meta:
        model = models.InterventionStatus

    label = Sequence(lambda n: "Status %s" % n)


class InterventionStakeFactory(django.DjangoModelFactory):
    class Meta:
        model = models.InterventionStake

    label = Sequence(lambda n: "Status %s" % n)


class InterventionDisorderFactory(django.DjangoModelFactory):
    class Meta:
        model = models.InterventionDisorder

    label = Sequence(lambda n: "Disorder %s" % n)


class InterventionTypeFactory(django.DjangoModelFactory):
    class Meta:
        model = models.InterventionType

    label = Sequence(lambda n: "Type %s" % n)


class InterventionFactory(django.DjangoModelFactory):
    class Meta:
        model = models.Intervention

    name = Sequence(lambda n: "Intervention %s" % n)
    intervention_status = SubFactory(InterventionStatusFactory)
    intervention_type = SubFactory(InterventionTypeFactory)
    stake = SubFactory(InterventionStakeFactory)

    @post_generation
    def create_intervention(obj, create, extracted, **kwargs):
        if obj.pk:
            obj.disorders.add(InterventionDisorderFactory.create())


class InterventionWithTargetFactory(InterventionFactory):
    class Meta:
        model = models.Intervention

    @post_generation
    def create_target_intervention(obj, create, extracted, **kwargs):
        land = LandFactory.create(geom='SRID=2154;POINT (700040 6600040)')
        obj.target = land
        if create:
            obj.save()

    @post_generation
    def with_stream(obj, create, with_stream):
        # First generate create_target_intervention and then with stream.
        # We add the with stream here and do not use WithStreamFactory because it needs to be after
        # create_target_intervention
        if not create or not with_stream:
            return
        if with_stream and obj.geom:
            # Status / Morphology is already on a stream
            # It should not add this next stream in distance to source
            StreamFactory.create(geom_around=obj.geom)