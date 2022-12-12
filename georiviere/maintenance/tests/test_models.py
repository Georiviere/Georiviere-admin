from datetime import date
from django.test import TestCase

from georiviere.maintenance.tests.factories import InterventionFactory


class InterventionTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.intervention = InterventionFactory.create(
            name="Stop rolling stone",
            date=date(2022, 11, 25),
        )

    def test_str(self):
        self.assertEqual(str(self.intervention), "Stop rolling stone (2022-11-25)")
