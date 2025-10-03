from django.test import TestCase

from geotrek.authent.tests.factories import StructureFactory

from georiviere.tests.factories import UserAllPermsFactory
from georiviere.knowledge.forms import KnowledgeForm
from . import factories


class KnowledgeFormTest(TestCase):
    """Test knowledge forms"""

    @classmethod
    def setUpTestData(cls):
        cls.user = UserAllPermsFactory(password='booh')
        cls.knowledge = factories.KnowledgeFactory()

    def test_update_knowledge(self):
        """Test create new knowledge"""
        data = {
            'structure': self.knowledge.structure,
            'name': 'New name',
            'description': self.knowledge.description,
            'geom': self.knowledge.geom.ewkt,
        }
        knowledge_form_update = KnowledgeForm(
            user=self.user,
            instance=self.knowledge,
            data=data
        )
        self.assertTrue(knowledge_form_update.is_valid())
