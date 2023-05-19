from factory import django, fuzzy, SubFactory, Sequence
from mapentity.tests.factories import PointFactory

from georiviere.contribution import models


class ContributionFactory(PointFactory):
    class Meta:
        model = models.Contribution

    name_author = fuzzy.FuzzyText()
    email_author = Sequence(lambda n: f"mail{n}@mail.mail")
    date_observation = '2020-03-17T00:00:00Z'


class ContributionPotentialDamageFactory(django.DjangoModelFactory):
    class Meta:
        model = models.ContributionPotentialDamage

    contribution = SubFactory(ContributionFactory)


class ContributionLandscapeElementsFactory(django.DjangoModelFactory):
    class Meta:
        model = models.ContributionLandscapeElements

    contribution = SubFactory(ContributionFactory)


class ContributionCategoryFactory(django.DjangoModelFactory):
    class Meta:
        model = models.ContributionCategory

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
