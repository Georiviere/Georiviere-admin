from collections import OrderedDict

from django.contrib.contenttypes.models import ContentType
from geotrek.authent.tests.factories import StructureFactory

from georiviere.tests import CommonRiverTest
from georiviere.maintenance.models import Intervention
from georiviere.maintenance.tests.factories import (
    InterventionFactory, InterventionStatusFactory,
    InterventionDisorderFactory, InterventionStakeFactory, InterventionWithTargetFactory
)
from georiviere.knowledge.tests.factories import KnowledgeFactory


class InterventionViewsTest(CommonRiverTest):
    model = Intervention
    modelfactory = InterventionFactory

    def get_expected_json_attrs(self):
        return {
            'id': self.obj.pk,
            'description': self.obj.description,
            'name': self.obj.name,
            'disorders': [self.obj.disorders.all()[0].pk],
            'width': 0.0,
            'height': 0.0,
            'intervention_status': self.obj.intervention_status.pk,
            'intervention_type': self.obj.intervention_type.pk,
            'stake': self.obj.stake.pk,
        }

    def get_bad_data(self):
        return OrderedDict([
            ('name', ''),
            ('structure', ''),
        ]), 'This field is required.'

    def get_good_data(self):
        structure = StructureFactory.create()
        good_data = {
            'structure': structure.pk,
            'name': 'test',
            'date': '2012-08-23',
            'disorders': InterventionDisorderFactory.create().pk,
            'description': '',
            'slope': 0,
            'area': 0,
            'height': 0.0,
            'width': 0.0,
            'length': 0.0,
            'intervention_status': InterventionStatusFactory.create().pk,
            'stake': InterventionStakeFactory.create().pk,
        }
        return good_data


class InterventionWithTargetViewsTest(InterventionViewsTest):
    """Test Intervention linked to a target"""
    modelfactory = InterventionWithTargetFactory

    def get_good_data(self):
        """Test creation of an intervention not linked to a knowledge"""
        structure = StructureFactory.create()
        knowledge_object = KnowledgeFactory.create(
            structure=structure
        )
        knowledge_contenttype = ContentType.objects.get(model='knowledge')
        good_data = {
            'structure': structure.pk,
            'name': 'test',
            'date': '2012-08-23',
            'disorders': InterventionDisorderFactory.create().pk,
            'description': '',
            'slope': 0,
            'area': 0,
            'height': 0.0,
            'width': 0.0,
            'length': 0.0,
            'intervention_status': InterventionStatusFactory.create().pk,
            'stake': InterventionStakeFactory.create().pk,
            'target_type': knowledge_contenttype.pk,
            'target_id': knowledge_object.pk,
        }
        return good_data

    def test_detail_target_objects(self):
        self.login()
        structure = StructureFactory.create()
        knowledge_object = KnowledgeFactory.create(
            structure=structure
        )
        intervention_on_knowledge = InterventionFactory.create(target=knowledge_object)

        response = self.client.get(intervention_on_knowledge.get_detail_url())
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, intervention_on_knowledge.target_display)
