from datetime import date
from django.core.exceptions import ValidationError
from django.test import TestCase

from georiviere.maintenance.tests import factories

class InterventionTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.intervention = factories.InterventionFactory.create(
            name="Stop rolling stone",
            date=date(2022, 11, 25),
        )

    def test_str(self):
        self.assertEqual(str(self.intervention), "Stop rolling stone (2022-11-25)")
