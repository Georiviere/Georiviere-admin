from string import ascii_letters

from factory import django, fuzzy, enums, post_generation, SubFactory, Sequence

from georiviere.tests.factories import BaseLineStringFactory
from georiviere.river.models import Stream
from georiviere.river.tests.factories import TopologyFactory
from .. import models


class UsageFactory(BaseLineStringFactory):
    class Meta:
        model = models.Usage

    @post_generation
    def usage_types(obj, create, extracted=None, **kwargs):
        if create and extracted:
            obj.usage_types.set(extracted)


class UsageTypeFactory(django.DjangoModelFactory):
    class Meta:
        model = models.UsageType

    label = Sequence(lambda n: "Usage type %s" % n)


class MorphologyFactory(BaseLineStringFactory):
    topology = SubFactory(TopologyFactory)
    description = fuzzy.FuzzyText(length=200)

    class Meta:
        model = models.Morphology


class PlanLayoutTypeFactory(django.DjangoModelFactory):
    class Meta:
        model = models.PlanLayoutType

    label = Sequence(lambda n: 'Plan layout type {}'.format(n))


class HabitatTypeFactory(django.DjangoModelFactory):
    class Meta:
        model = models.HabitatType

    label = Sequence(lambda n: 'Habitat type {}'.format(n))


class HabitatsDiversityFactory(django.DjangoModelFactory):
    class Meta:
        model = models.HabitatsDiversity

    label = Sequence(lambda n: 'Habitats diversity {}'.format(n))


class BankStateFactory(django.DjangoModelFactory):
    class Meta:
        model = models.BankState

    label = Sequence(lambda n: 'Bank state {}'.format(n))


class SedimentDynamicFactory(django.DjangoModelFactory):
    class Meta:
        model = models.SedimentDynamic

    label = Sequence(lambda n: 'Sediment dynamic {}'.format(n))


class GranulometricDiversityFactory(django.DjangoModelFactory):
    class Meta:
        model = models.GranulometricDiversity

    label = Sequence(lambda n: 'Granulometric diversity {}'.format(n))


class FaciesDiversityFactory(django.DjangoModelFactory):
    class Meta:
        model = models.FaciesDiversity

    label = Sequence(lambda n: 'Facies diversity {}'.format(n))


class WorkingSpaceTypeFactory(django.DjangoModelFactory):
    class Meta:
        model = models.WorkingSpaceType

    label = Sequence(lambda n: 'Working space type {}'.format(n))


class FlowTypeFactory(django.DjangoModelFactory):
    class Meta:
        model = models.FlowType

    label = Sequence(lambda n: 'Flow type {}'.format(n))


class LandTypeFactory(django.DjangoModelFactory):
    class Meta:
        model = models.LandType

    label = Sequence(lambda n: 'Land type {}'.format(n))


class ControlTypeFactory(django.DjangoModelFactory):
    class Meta:
        model = models.ControlType

    label = Sequence(lambda n: f'Control type {n}')


class LandFactory(BaseLineStringFactory):
    class Meta:
        model = models.Land

    land_type = SubFactory(LandTypeFactory)
    control_type = SubFactory(ControlTypeFactory)
    owner = fuzzy.FuzzyText()
    description = fuzzy.FuzzyText(length=200)
    identifier = fuzzy.FuzzyText(chars=ascii_letters)


class StatusTypeFactory(django.DjangoModelFactory):
    class Meta:
        model = models.StatusType

    label = Sequence(lambda n: 'Status type {}'.format(n))


class StatusFactory(BaseLineStringFactory):
    class Meta:
        model = models.Status

    topology = SubFactory(TopologyFactory)
    description = fuzzy.FuzzyText(length=200)

    @post_generation
    def status_types(obj, create, extracted=None, **kwargs):
        if create and extracted:
            obj.status_types.set(extracted)


class StatusOnStreamFactory(BaseLineStringFactory):
    class Meta:
        model = Stream

    @classmethod
    def create(cls, **kwargs):
        stream = cls._generate(enums.CREATE_STRATEGY, kwargs)
        status = stream.topologies.filter(status__isnull=False).get().status
        return status
