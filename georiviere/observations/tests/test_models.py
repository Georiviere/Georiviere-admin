from django.test import TestCase

from . import factories
from georiviere.observations.models import ParameterTracking


class StationTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.station_profile = factories.StationProfileFactory()
        cls.station = factories.StationFactory(
            label="DOUBS A GEVRY",
            code="06031200",
            station_profiles=[cls.station_profile]
        )

    def test_str(self):
        self.assertEqual(str(self.station), "DOUBS A GEVRY (06031200)")

    def test_local_influence_display(self):
        self.assertEqual(self.station.local_influence_display, "Unknown")

    def test_station_profiles_display(self):
        self.assertEqual(self.station.station_profiles_display, str(self.station_profile))


class ParameterTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.station = factories.StationFactory(
            label="DOUBS A GEVRY",
            code="06031200"
        )
        cls.unit = factories.UnitFactory(
            code="123",
            label="mètre cube par seconde",
            symbol="m³/s",
        )
        cls.parameter_category1 = factories.ParameterCategoryFactory(
            label="Physique"
        )
        cls.parameter_category2 = factories.ParameterCategoryFactory(
            label="Chimique"
        )
        cls.parameter1 = factories.ParameterFactory(
            label="Débit instantané",
            unit=cls.unit,
            categories=(cls.parameter_category1, cls.parameter_category2),
        )
        cls.parameter2 = factories.ParameterFactory(
            label="Nutriments",
            unit=None,
            categories=(cls.parameter_category2,),
        )
        cls.parameter_tracking = factories.ParameterTrackingFactory(
            label="Suivi hydro",
            station=cls.station,
            parameter=cls.parameter1,
        )

    def test_str_parametertracking(self):
        self.assertEqual(
            str(self.parameter_tracking),
            "Suivi hydro"
        )

    def test_str_unit(self):
        self.assertEqual(
            str(self.unit),
            "m³/s"
        )

    def test_str_parameter_category(self):
        self.assertEqual(
            str(self.parameter_category1),
            "Physique"
        )

    def test_str_parameter(self):
        self.assertEqual(
            str(self.parameter1),
            "Débit instantané (m³/s)"
        )
        self.assertEqual(
            str(self.parameter2),
            "Nutriments"
        )

    def test_get_station_parameters_tracked(self):
        self.assertEqual(
            self.station.get_parameters_tracked().first(),
            self.parameter_tracking
        )
