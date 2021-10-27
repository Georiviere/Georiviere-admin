import json
import requests
from io import StringIO
from unittest import mock

from django.core.management import call_command
from django.core.management.base import CommandError
from django.test import TestCase
from django.conf import settings

from observations.models import Station, StationProfile, Unit

TEST_DATA_PATH = settings.BASE_DIR / 'observations' / 'tests' / 'data'


def requests_get_mock_response(*args, **kwargs):
    """Build mock_response with test file data, according to api_url"""
    # Get filename from api_url
    filename = TEST_DATA_PATH / 'response_api_hydrometrie_stations.json'
    if "urf" in args[0]:
        filename = TEST_DATA_PATH / 'response_sandre_urf.json'
    if "hydrometrie" in args[0]:
        filename = TEST_DATA_PATH / 'response_api_hydrometrie_stations.json'
    if "temperature" in args[0]:
        filename = TEST_DATA_PATH / 'response_api_temperature_stations.json'
    if "station_pc" in args[0]:
        filename = TEST_DATA_PATH / 'response_api_pcquality_stations.json'
    if "analyse_pc" in args[0]:
        filename = TEST_DATA_PATH / 'response_api_pcquality_analyse.json'

    # Build response
    mock_response = mock.Mock()
    with open(filename, 'r') as f:
        expected_dict = json.load(f)
    mock_response.json.return_value = expected_dict
    mock_response.status_code = 200
    return mock_response


def requests_get_mock_response_500(*args, **kwargs):
    """Build mock_response like if server is down"""
    # Build response
    mock_response = mock.Mock()
    mock_response.status_code = 500
    return mock_response


@mock.patch.object(requests, 'get', side_effect=requests_get_mock_response)
class ImportReferentielTest(TestCase):
    """Test import_reference_data command
    Unit only for now
    """
    def test_urf_imported(self, mock_get):
        """Test references units import"""
        # Call command
        out = StringIO()
        call_command('import_reference_data', verbosity=2, stdout=out)

        units = Unit.objects.all()
        self.assertEqual(units.count(), 2)
        unit = units.get(code="165")
        self.assertEqual(unit.label, "milligramme de dichlore par litre")
        self.assertEqual(unit.symbol, "mg(Cl2)/L")

        self.assertIn('Get reference unit from API', out.getvalue())
        self.assertIn('Import 2 units from API', out.getvalue())
        self.assertIn('Created unit mg(Cl2)/L', out.getvalue())


@mock.patch.object(requests, 'get', side_effect=requests_get_mock_response)
class ImportStationTest(TestCase):
    """Test import_station command
    Test datas are from LABERGEMENT-STE-MARIE
    """

    def test_hydrometric_stations_imported(self, mock_get):
        out = StringIO()

        # Call command
        call_command('import_hydrometric_stations', stdout=out)

        # Check stations imported
        stations = Station.objects.all()
        self.assertEqual(stations.count(), 2)
        station = stations.get(code="U201201001")
        hydro_station_profile = StationProfile.objects.get(code='HYDRO') or None
        self.assertIn(hydro_station_profile, station.station_profiles.all())
        self.assertEqual(station.label, "Le Doubs à Labergement-Sainte-Marie")
        self.assertEqual(station.site_code, "U2012010")
        self.assertEqual(station.purpose_code, "12")
        self.assertEqual(station.description, "Lorem Ipsum")
        self.assertEqual(station.station_uri, "https://id.eaufrance.fr/StationHydro/U201201001")
        self.assertTrue(station.in_service)
        self.assertEqual(station.local_influence, 1)

        # For default values
        station = stations.get(code="U201541001")
        self.assertFalse(station.in_service)
        self.assertEquals(station.purpose_code, "")

    def test_pcquality_stations_imported(self, mock_get):
        # Call command
        out = StringIO()
        call_command('import_pcquality_stations', stdout=out)

        # Check stations imported
        stations = Station.objects.all()
        self.assertEqual(stations.count(), 10)
        station = stations.get(code="06017140")
        pcquality_station_profile = StationProfile.objects.get(code='PCQUAL') or None
        self.assertIn(pcquality_station_profile, station.station_profiles.all())
        self.assertEqual(station.label, "DOUBS A LABERGEMENT-STE-MARIE 2")
        self.assertEqual(station.code, "06017140")
        self.assertEqual(station.station_uri, "http://id.eaufrance.fr/STQ/06017140")
        self.assertEqual(station.hardness, None)
        self.assertEquals(station.in_service, None)

    def test_temperature_stations_imported(self, mock_get):

        # Call command
        out = StringIO()
        call_command('import_temperature_stations', stdout=out)

        # Check stations imported
        stations = Station.objects.all()
        self.assertEqual(stations.count(), 2)
        station = stations.get(code="06017200")
        temp_station_profile = StationProfile.objects.get(code='TEMP') or None
        self.assertIn(temp_station_profile, station.station_profiles.all())
        self.assertEqual(station.label, "DOUBS A LABERGEMENT-STE-MARIE 1")
        self.assertEqual(station.code, "06017200")
        self.assertEqual(station.station_uri, "http://id.eaufrance.fr/STQ/06017200")


@mock.patch.object(requests, 'get', side_effect=requests_get_mock_response)
class ImportStationVerboseTest(TestCase):
    """Test import_station command with verbosity
    Test datas are from LABERGEMENT-STE-MARIE
    """

    def test_temperature_stations_imported(self, mock_get):
        out = StringIO()

        # Call command
        call_command('import_temperature_stations', verbosity=2, stdout=out)
        self.assertIn('Get station from API', out.getvalue())
        self.assertIn('Import 2 stations from API', out.getvalue())


@mock.patch.object(requests, 'get', side_effect=requests_get_mock_response_500)
class ImportStationServerDownTest(TestCase):
    """Test import_station command with verbosity
    Test datas are from LABERGEMENT-STE-MARIE
    """

    def test_temperature_stations_imported(self, mock_get):
        out = StringIO()

        # Call command
        with self.assertRaises(CommandError):
            call_command('import_temperature_stations', verbosity=2, stdout=out)


@mock.patch.object(requests, 'get', side_effect=requests_get_mock_response)
class ImportStationAllRedoTest(TestCase):
    """Test import_station command
    Test datas are from LABERGEMENT-STE-MARIE
    """

    def test_import_all_stations(self, mock_get):
        """Test import all stations PC Quality and temperature,
        since some are the same with differnt profiles"""

        # Call command
        out = StringIO()
        call_command('import_pcquality_stations', stdout=out)

        # Call command again
        call_command('import_temperature_stations', stdout=out)

        stations = Station.objects.all()
        self.assertEqual(stations.count(), 11)

    def test_redo_import_hydrometric_stations(self, mock_get):
        """Test import twice hydrometric stations"""

        # Call command
        out = StringIO()
        call_command('import_hydrometric_stations', verbosity=2, stdout=out)

        # Check output
        self.assertIn('Get station from API', out.getvalue())
        self.assertIn('Import 2 stations from API', out.getvalue())
        self.assertIn('Created station profile  (HYDRO)', out.getvalue())
        self.assertIn('Created station Le ruisseau du Lhaut à Labergement-Sainte-Marie (U201541001)', out.getvalue())

        # Call command a second time
        call_command('import_hydrometric_stations', verbosity=2, stdout=out)
        # Check output
        self.assertIn('Updated station Le ruisseau du Lhaut à Labergement-Sainte-Marie (U201541001)', out.getvalue())

    def test_redo_import_pcquality_stations(self, mock_get):
        """Test import twice pcquality stations"""

        # Call command
        out = StringIO()
        call_command('import_pcquality_stations', verbosity=2, stdout=out)

        # Check output
        self.assertIn('Created station profile  (PCQUAL)', out.getvalue())
        self.assertIn('Created station DOUBS A LABERGEMENT-STE-MARIE 2 (06017140)', out.getvalue())

        # Call command a second time
        call_command('import_pcquality_stations', verbosity=2, stdout=out)
        # Check output
        self.assertIn('Updated station DOUBS A LABERGEMENT-STE-MARIE 2 (06017140)', out.getvalue())

    def test_redo_import_temperature_stations(self, mock_get):
        """Test import twice temperature stations"""

        # Call command
        out = StringIO()
        call_command('import_temperature_stations', verbosity=2, stdout=out)

        # Check output
        self.assertIn('Created station profile  (TEMP)', out.getvalue())
        self.assertIn('Created station DOUBS A LABERGEMENT-STE-MARIE 1 (06017200)', out.getvalue())

        # Call command a second time
        call_command('import_temperature_stations', verbosity=2, stdout=out)
        # Check output
        self.assertIn('Updated station DOUBS A LABERGEMENT-STE-MARIE 1 (06017200)', out.getvalue())


@mock.patch.object(requests, 'get', side_effect=requests_get_mock_response)
class ImportStationWithParametersTest(TestCase):
    """Test import_station command with parameters
    Test datas are from LABERGEMENT-STE-MARIE
    """

    def test_import_temperature_stations_with_parameters(self, mock_get):
        # Call command with parameters
        out = StringIO()
        call_command('import_temperature_stations',
                     verbosity=2,
                     with_parameters=True,
                     stdout=out)

        # Check stations imported
        stations = Station.objects.all()
        station = stations.get(code="06017200")
        parameter_tracking_set = station.parametertracking_set.all()
        self.assertEqual(parameter_tracking_set.count(), 1)
        self.assertEqual(parameter_tracking_set[0].parameter.label, "Température de l'Eau")
        self.assertEqual(parameter_tracking_set[0].parameter.unit.symbol, "°C")

        # Check output
        self.assertIn("Added parameter Chronique température", out.getvalue())

    def test_import_pcquality_stations_with_parameters(self, mock_get):
        # Call command with parameters
        out = StringIO()
        call_command('import_pcquality_stations',
                     verbosity=2,
                     with_parameters=True,
                     stdout=out)

        # Check stations imported
        stations = Station.objects.all()
        station = stations.get(code="06017140")
        parameters_tracked = station.parametertracking_set.all()
        self.assertEqual(parameters_tracked.count(), 16)
        self.assertEqual(parameters_tracked.filter(parameter__label='pH').count(), 1)
        self.assertEqual(parameters_tracked.get(parameter__label='pH').parameter.unit.symbol, "unité pH")

        # Check output
        self.assertIn("Added parameter pH", out.getvalue())
