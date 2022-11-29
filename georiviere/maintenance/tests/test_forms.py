from datetime import date
from django.core.exceptions import ValidationError
from django.test import TestCase

from geotrek.authent.tests.factories import StructureFactory
from georiviere.maintenance.tests.factories import (
    InterventionDisorderFactory, InterventionStatusFactory,
    InterventionStakeFactory
)
from georiviere.tests.factories import UserAllPermsFactory
from georiviere.river.tests.factories import StreamFactory
from georiviere.maintenance.forms import InterventionForm

class InterventionTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.user = UserAllPermsFactory(password='booh')
        cls.stream = StreamFactory.create()

    def test_create_standalone_intervention(self):
        """Test creation of an intervention not linked to a knowledge"""

        user = UserAllPermsFactory(password='booh')
        structure = StructureFactory.create()
        data = {
            'structure': structure,
            'name': 'test',
            'date': '2012-08-23',
            'disorders': [InterventionDisorderFactory.create()],
            'description': '',
            'slope': 0,
            'area': 0,
            'height': 0.0,
            'width': 0.0,
            'length': 0.0,
            'intervention_status': InterventionStatusFactory.create(),
            'stake': InterventionStakeFactory.create(),
        }
        intervention_add_form = InterventionForm(
            user=user,
            data=data
        )
        self.assertTrue(intervention_add_form.is_valid())
