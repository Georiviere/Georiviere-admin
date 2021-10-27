from datetime import date, timedelta

from factory import post_generation, django, fuzzy, Sequence, SubFactory

from django.contrib.gis.geos import Point

from . import models


class StationProfileFactory(django.DjangoModelFactory):
    class Meta:
        model = models.StationProfile

    code = Sequence(lambda n: 'STP{}'.format(n))
    label = fuzzy.FuzzyText()


class StationFactory(django.DjangoModelFactory):
    class Meta:
        model = models.Station

    code = Sequence(lambda n: '0603120{}'.format(n))
    label = fuzzy.FuzzyText()
    geom = Point(886281, 6662370)

    @post_generation
    def station_profiles(obj, create, extracted=None, **kwargs):
        if create:
            if extracted:
                obj.categories.add(*extracted)


class UnitFactory(django.DjangoModelFactory):
    class Meta:
        model = models.Unit

    code = fuzzy.FuzzyText(length=6)
    label = fuzzy.FuzzyText(length=15)
    symbol = fuzzy.FuzzyText(length=4)


class ParameterCategoryFactory(django.DjangoModelFactory):
    class Meta:
        model = models.ParameterCategory

    code = fuzzy.FuzzyText(length=6)
    label = fuzzy.FuzzyText(length=15)
    definition = fuzzy.FuzzyText(length=250)


class ParameterFactory(django.DjangoModelFactory):
    class Meta:
        model = models.Parameter

    code = fuzzy.FuzzyText(length=6)
    label = fuzzy.FuzzyText(length=15)
    definition = fuzzy.FuzzyText(length=250)
    unit = SubFactory(UnitFactory)

    @post_generation
    def categories(obj, create, extracted=None, **kwargs):
        if create:
            if extracted:
                obj.categories.add(*extracted)


class ParameterTrackingFactory(django.DjangoModelFactory):
    class Meta:
        model = models.ParameterTracking

    label = fuzzy.FuzzyText(length=150)
    parameter = SubFactory(ParameterFactory)
    station = SubFactory(StationFactory)
    measure_frequency = fuzzy.FuzzyText(length=150)
    transmission_frequency = fuzzy.FuzzyText(length=150)
    measure_start_date = fuzzy.FuzzyDate(start_date=date.today() - timedelta(1000), end_date=date.today())
    measure_end_date = fuzzy.FuzzyDate(start_date=date.today(), end_date=date.today() + timedelta(1000))
