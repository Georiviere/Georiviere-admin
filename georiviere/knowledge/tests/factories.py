from factory import django, fuzzy, SubFactory, Sequence
from mapentity.tests.factories import PointFactory

from georiviere.knowledge import models
from georiviere.river.tests.factories import WithStreamFactory


class KnowledgeTypeFactory(django.DjangoModelFactory):
    class Meta:
        model = models.KnowledgeType

    label = fuzzy.FuzzyText()


class KnowledgeFactory(WithStreamFactory, PointFactory):
    class Meta:
        model = models.Knowledge

    code = fuzzy.FuzzyText(length=12)
    name = fuzzy.FuzzyText(length=12)
    description = fuzzy.FuzzyText()
    knowledge_type = SubFactory(KnowledgeTypeFactory)


class VegetationTypeFactory(django.DjangoModelFactory):
    class Meta:
        model = models.VegetationType

    label = fuzzy.FuzzyText()


class WorkTypeFactory(django.DjangoModelFactory):
    class Meta:
        model = models.WorkType

    label = fuzzy.FuzzyText()


class WorkMaterialFactory(django.DjangoModelFactory):
    class Meta:
        model = models.WorkMaterial

    label = fuzzy.FuzzyText()


class FollowUpTypeFactory(django.DjangoModelFactory):
    class Meta:
        model = models.FollowUpType

    label = Sequence(lambda n: "Type %s" % n)


class FollowUpFactory(django.DjangoModelFactory):
    class Meta:
        model = models.FollowUp

    name = Sequence(lambda n: "Follow-up %s" % n)
    followup_type = SubFactory(FollowUpTypeFactory)


class FollowUpKnowledgeFactory(FollowUpFactory):
    knowledge = SubFactory(KnowledgeFactory)
