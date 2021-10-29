from django.test import TestCase

from georiviere.observations.models import Parameter, ParameterTracking
from . import factories


class PerformanceTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.parameters = factories.ParameterFactory.create_batch(10)
        cls.parameters = factories.ParameterTrackingFactory.create_batch(10)

    def test_str_parameters_number_queries(self):
        """Test queries number when str each parameter"""

        with self.assertNumQueries(1):
            [str(el) for el in Parameter.objects.all()]

    def test_str_parameters_tracking_number_queries(self):
        """Test queries number when str each parameter"""

        with self.assertNumQueries(1):
            [str(el) for el in ParameterTracking.objects.all()]
