from django.test import TestCase
from geotrek.authent.factories import StructureFactory

from observations.filters import StationFilterSet
from observations.tests.factories import StationFactory, ParameterFactory, ParameterTrackingFactory


class StationFilterTestCase(TestCase):
    """Test filter on parameter tracked"""

    def setUp(self):
        self.structure = StructureFactory.create()
        self.station1 = StationFactory.create(
            structure=self.structure,
        )
        self.station2 = StationFactory.create(
            structure=self.structure,
        )
        self.station3 = StationFactory.create(
            structure=self.structure,
            in_service=False,
        )
        self.station4 = StationFactory.create(
            structure=self.structure,
            in_service=True,
        )
        self.parameter1 = ParameterFactory.create()
        self.parameter2 = ParameterFactory.create()
        self.parameter_tracked_1 = ParameterTrackingFactory.create(
            station=self.station1,
            parameter=self.parameter1
        )
        self.parameter_tracked_2 = ParameterTrackingFactory.create(
            station=self.station2,
            parameter=self.parameter2
        )
        self.filterset_class = StationFilterSet

    def test_filter_station_on_parameter(self):
        """Test filter on parameter tracked"""
        filterset = self.filterset_class({'parameters_tracked': [self.parameter1]})
        self.assertEqual(filterset.qs.count(), 1)

    def test_filter_station_in_service_true(self):
        """Test filter on stations in service"""
        filterset = self.filterset_class({'in_service': True})
        self.assertEqual(filterset.qs.count(), 1)

    def test_filter_station_in_service_false(self):
        """Test filter on stations not in service"""
        filterset = self.filterset_class({'in_service': False})
        self.assertEqual(filterset.qs.count(), 1)

    def test_filter_station_in_service_unknown(self):
        """Test filter on stations in service"""
        filterset = self.filterset_class({'in_service': "null"})
        self.assertEqual(filterset.qs.count(), 2)
