from collections import OrderedDict

from geotrek.authent.tests.factories import StructureFactory

from georiviere.tests import CommonRiverTest
from georiviere.observations.models import Station, ParameterTracking
from .factories import (
    StationFactory, StationProfileFactory, ParameterFactory
)


class StationViewTestCase(CommonRiverTest):
    model = Station
    modelfactory = StationFactory

    def get_expected_json_attrs(self):
        return {
            'annex_uri': '',
            'id': self.obj.pk,
            'code': self.obj.code,
            'date_insert': '2020-03-17T00:00:00Z',
            'date_update': '2020-03-17T00:00:00Z',
            'description': self.obj.description,
            'geom': self.obj.geom.ewkt,
            'hardness': self.obj.hardness,
            'in_service': self.obj.in_service,
            'label': self.obj.label,
            'local_influence': self.obj.local_influence,
            'operations_uri': '',
            'purpose_code': self.obj.purpose_code,
            'site_code': self.obj.site_code,
            'station_profiles': [],
            'structure': self.obj.structure.pk,
            'station_uri': self.obj.station_uri,
        }

    def get_bad_data(self):
        return OrderedDict([
            ('label', ''),
            ('parametertracking_set-TOTAL_FORMS', '0'),
            ('parametertracking_set-INITIAL_FORMS', '1'),
            ('parametertracking_set-MAX_NUM_FORMS', '0'),
        ]), 'This field is required.'

    def get_good_data(self):
        structure = StructureFactory.create()
        station_profile = StationProfileFactory.create()
        temp_data = self.modelfactory.build(
            structure=structure,
            station_profiles=[station_profile]
        )
        return {
            'structure': structure.pk,
            'geom': '{"geom": "%s", "snap": [%s]}' % (temp_data.geom.transform(4326, clone=True).ewkt,
                                                      ','.join(['null'])),
            'code': '1234',
            'label': 'test',
            'station_profiles': [station_profile.pk],
            'local_influence': Station.LocalInfluenceChoices.UNKNOWN,
            'operations_uri': 'https://fad.dtr',
            'annex_uri': 'https://fad.dtr',
            'parametertracking_set-TOTAL_FORMS': '2',
            'parametertracking_set-INITIAL_FORMS': '0',
            'parametertracking_set-MAX_NUM_FORMS': '',

            'parametertracking_set-0-label': 'Paramètre suivi Ted',
            'parametertracking_set-0-parameter': ParameterFactory.create().pk,
            'parametertracking_set-0-measure_frequency': 'par jour',
            'parametertracking_set-0-transmission_frequency': 'par semaine',
            'parametertracking_set-0-data_availability': ParameterTracking.DataAvailabilityChoice.ONDEMAND,
            'parametertracking_set-0-measure_start_date': '2019-06-06',
            'parametertracking_set-0-measure_end_date': '2020-06-06',
            'parametertracking_set-0-id': '',
            'parametertracking_set-0-DELETE': '',

            'parametertracking_set-1-label': 'Paramètre suivi Bob',
            'parametertracking_set-1-parameter': ParameterFactory.create().pk,
            'parametertracking_set-1-measure_frequency': '',
            'parametertracking_set-1-transmission_frequency': '',
            'parametertracking_set-1-data_availability': ParameterTracking.DataAvailabilityChoice.ONDEMAND,
            'parametertracking_set-1-measure_start_date': '',
            'parametertracking_set-1-measure_end_date': '',
            'parametertracking_set-1-id': '',
            'parametertracking_set-1-DELETE': '',
        }

    def test_listing_number_queries(self):
        """Test number queries when get list object"""
        self.login()
        self.modelfactory.create_batch(100)

        with self.assertNumQueries(7):
            self.client.get(self.model.get_jsonlist_url())

        with self.assertNumQueries(6):
            self.client.get(self.model.get_format_list_url())

    def test_detail_number_queries(self):
        """Test number queries when get detail object"""
        self.login()
        station = self.modelfactory.create()

        with self.assertNumQueries(52):
            self.client.get(station.get_detail_url())
