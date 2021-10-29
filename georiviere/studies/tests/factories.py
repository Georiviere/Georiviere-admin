from factory import django, fuzzy, post_generation

from georiviere.tests.factories import PointFactory
from .. import models


class StudyTypeFactory(django.DjangoModelFactory):
    class Meta:
        model = models.StudyType

    label = fuzzy.FuzzyText()


class StudyFactory(PointFactory):
    class Meta:
        model = models.Study

    title = fuzzy.FuzzyText(length=150)
    description = fuzzy.FuzzyText()
    study_authors = fuzzy.FuzzyText()
    year = fuzzy.FuzzyInteger(low=1850, high=2021)

    @post_generation
    def study_types(obj, create, extracted=None, **kwargs):
        if create:
            if extracted:
                obj.study_types.add(*extracted)
