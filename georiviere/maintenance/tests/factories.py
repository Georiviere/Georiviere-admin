from factory import django, Sequence, SubFactory, post_generation

from georiviere.maintenance import models


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
