from factory import django, fuzzy, SubFactory, Sequence
from mapentity.tests.factories import PointFactory

from georiviere.contribution import models
from georiviere.portal.tests.factories import PortalFactory


class ContributionStatusFactory(django.DjangoModelFactory):
    class Meta:
        model = models.ContributionStatus

    label = Sequence(lambda n: f'Contribution status {n}')


class ContributionFactory(PointFactory):
    class Meta:
        model = models.Contribution

    name_author = fuzzy.FuzzyText()
    email_author = Sequence(lambda n: f"mail{n}@mail.mail")
    date_observation = '2020-03-17T00:00:00Z'
    portal = SubFactory(PortalFactory)


class ContributionPotentialDamageFactory(django.DjangoModelFactory):
    class Meta:
        model = models.ContributionPotentialDamage

    contribution = SubFactory(ContributionFactory)


class ContributionLandscapeElementsFactory(django.DjangoModelFactory):
    class Meta:
        model = models.ContributionLandscapeElements

    contribution = SubFactory(ContributionFactory)


class ContributionQualityFactory(django.DjangoModelFactory):
    class Meta:
        model = models.ContributionQuality

    contribution = SubFactory(ContributionFactory)


class ContributionQuantityFactory(django.DjangoModelFactory):
    class Meta:
        model = models.ContributionQuantity

    contribution = SubFactory(ContributionFactory)


class ContributionFaunaFloraFactory(django.DjangoModelFactory):
    class Meta:
        model = models.ContributionFaunaFlora

    contribution = SubFactory(ContributionFactory)


class SeverityTypeTypeFactory(django.DjangoModelFactory):
    class Meta:
        model = models.SeverityType

    label = Sequence(lambda n: f'Severity type {n}')


class LandingTypeFactory(django.DjangoModelFactory):
    class Meta:
        model = models.LandingType

    label = Sequence(lambda n: f'Landing type {n}')


class JamTypeFactory(django.DjangoModelFactory):
    class Meta:
        model = models.JamType

    label = Sequence(lambda n: f'Jam type {n}')


class DiseaseTypeFactory(django.DjangoModelFactory):
    class Meta:
        model = models.DiseaseType

    label = Sequence(lambda n: f'Disease type {n}')


class DeadSpeciesFactory(django.DjangoModelFactory):
    class Meta:
        model = models.DeadSpecies

    label = Sequence(lambda n: f'Dead species {n}')


class InvasiveSpeciesFactory(django.DjangoModelFactory):
    class Meta:
        model = models.InvasiveSpecies

    label = Sequence(lambda n: f'Invasive species {n}')


class HeritageSpeciesFactory(django.DjangoModelFactory):
    class Meta:
        model = models.HeritageSpecies

    label = Sequence(lambda n: f'Heritage species {n}')


class HeritageObservationFactory(django.DjangoModelFactory):
    class Meta:
        model = models.HeritageObservation

    label = Sequence(lambda n: f'Heritage observation {n}')


class FishSpeciesFactory(django.DjangoModelFactory):
    class Meta:
        model = models.FishSpecies

    label = Sequence(lambda n: f'Fish species {n}')


class NaturePollutionFactory(django.DjangoModelFactory):
    class Meta:
        model = models.NaturePollution

    label = Sequence(lambda n: f'Nature pollution {n}')


class TypePollutionFactory(django.DjangoModelFactory):
    class Meta:
        model = models.TypePollution

    label = Sequence(lambda n: f'Type pollution {n}')
