import factory

from mapentity.tests.factories import PointFactory

from geotrek.authent.tests.factories import StructureFactory

from georiviere.valorization.models import POIAction, POIActionType, POIKnowledge, POIKnowledgeType


class POIKnowledgeTypeFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = POIKnowledgeType

    label = factory.Sequence(lambda n: f'POI Knowledge type {n}')


class POIKnowledgeFactory(PointFactory):
    name = factory.Sequence(lambda n: f'name {n}')
    description = factory.Sequence(lambda n: f'description {n}')
    type = factory.SubFactory(POIKnowledgeTypeFactory)
    structure = factory.SubFactory(StructureFactory)

    class Meta:
        model = POIKnowledge


class POIActionTypeFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = POIActionType

    label = factory.Sequence(lambda n: f'POI Action type {n}')


class POIActionFactory(PointFactory):
    name = factory.Sequence(lambda n: f'name {n}')
    description = factory.Sequence(lambda n: f'description {n}')
    type = factory.SubFactory(POIActionTypeFactory)
    structure = factory.SubFactory(StructureFactory)

    class Meta:
        model = POIAction
