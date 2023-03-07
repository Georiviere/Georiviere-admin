import factory
from django.contrib.contenttypes.models import ContentType
from factory import fuzzy
from georiviere.maintenance.tests.factories import InterventionStatusFactory
from georiviere.observations.tests.factories import StationFactory
from georiviere.studies.tests.factories import StudyFactory

from georiviere.finances_administration import models
from georiviere.river.tests.factories import WithStreamFactory


class AdministrativeDeferralFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.AdministrativeDeferral

    label = factory.Sequence(lambda n: "Deferral %s" % n)


class OrganismFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.Organism

    name = factory.Sequence(lambda n: "Organism %s" % n)


class AdministrativeFileTypeFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.AdministrativeFileType

    label = factory.Sequence(lambda n: "Type %s" % n)


class AdministrativeFileDomainFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.AdministrativeFileDomain

    label = factory.Sequence(lambda n: "Domain %s" % n)


class AdministrativeFileFactory(WithStreamFactory, factory.django.DjangoModelFactory):
    class Meta:
        model = models.AdministrativeFile

    name = factory.Sequence(lambda n: "AdministrativeFile %s" % n)
    begin_date = '2010-01-01'
    end_date = '2012-01-01'


class AdministrativeFilePhaseFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.AdministrativePhase

    name = factory.Sequence(lambda n: "AdministrativePhase %s" % n)
    administrative_file = factory.SubFactory(AdministrativeFileFactory)
    estimated_budget = fuzzy.FuzzyDecimal(0, 100000, 2)
    revised_budget = fuzzy.FuzzyDecimal(0, 100000, 2)


class AdministrativeFileOperationFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.AdministrativeOperation
        exclude = ['content_object']
        abstract = True

    object_id = factory.SelfAttribute('content_object.id')
    content_type = factory.LazyAttribute(
        lambda o: ContentType.objects.get_for_model(o.content_object))

    administrative_file = factory.SubFactory(AdministrativeFileFactory)
    operation_status = factory.SubFactory(InterventionStatusFactory)
    estimated_cost = fuzzy.FuzzyDecimal(0, 100000, 2)
    material_cost = fuzzy.FuzzyDecimal(0, 100000, 2)
    subcontract_cost = fuzzy.FuzzyDecimal(0, 100000, 2)


class StudyOperationFactory(AdministrativeFileOperationFactory):
    class Meta:
        model = models.AdministrativeOperation

    content_object = factory.SubFactory(StudyFactory)


class StationOperationFactory(AdministrativeFileOperationFactory):
    class Meta:
        model = models.AdministrativeOperation

    content_object = factory.SubFactory(StationFactory)


class FundingFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.Funding

    amount = fuzzy.FuzzyDecimal(0, 9999, 2)
    administrative_file = factory.SubFactory(AdministrativeFileFactory)
    organism = factory.SubFactory(OrganismFactory)


class JobCategoryFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.JobCategory

    label = factory.Sequence(lambda n: "Job category %s" % n)
    man_day_cost = fuzzy.FuzzyDecimal(500, 800, 2)


class ManDayFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.ManDay

    nb_days = 1
    job_category = factory.SubFactory(JobCategoryFactory)
