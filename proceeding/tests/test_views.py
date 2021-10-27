from collections import OrderedDict

from django.test import override_settings
from tempfile import TemporaryDirectory

from georiviere.tests import CommonRiverTest

from proceeding.models import Proceeding
from proceeding.tests.factories import ProceedingFactory, EventTypeFactory

from geotrek.authent.factories import StructureFactory


@override_settings(MEDIA_ROOT=TemporaryDirectory().name)
class ProceedingViewTestCase(CommonRiverTest):
    model = Proceeding
    modelfactory = ProceedingFactory

    def get_expected_json_attrs(self):
        return {
            'id': self.obj.pk,
            'structure': self.obj.structure.pk,
            'name': self.obj.name,
            'date': '2002-02-20',
            'date_insert': '2020-03-17T00:00:00Z',
            'date_update': '2020-03-17T00:00:00Z',
            'description': self.obj.description,
            'eid': self.obj.eid,
            'length': self.obj.length,
            'geom_3d': self.obj.geom_3d.ewkt,
            'ascent': self.obj.ascent,
            'descent': self.obj.descent,
            'min_elevation': self.obj.min_elevation,
            'max_elevation': self.obj.max_elevation,
            'slope': 0.0,
            'geom': self.obj.geom.ewkt,
        }

    def get_bad_data(self):
        return OrderedDict([
            ('name', ''),
            ('events-TOTAL_FORMS', '0'),
            ('events-INITIAL_FORMS', '1'),
            ('events-MAX_NUM_FORMS', '0'),
        ]), 'This field is required.'

    def get_good_data(self):
        structure = StructureFactory.create()
        event_type1 = EventTypeFactory.create()
        event_type2 = EventTypeFactory.create()
        temp_data = self.modelfactory.build(structure=structure)
        return {
            'structure': structure.pk,
            'geom': temp_data.geom.ewkt,
            'eid': '2',
            'description': "5",
            'name': 'Name',
            'date': '2002-02-25',

            'events-TOTAL_FORMS': '2',
            'events-INITIAL_FORMS': '0',
            'events-MAX_NUM_FORMS': '0',

            'events-0-event_type': event_type1.pk,
            'events-0-date': '2020-03-12',
            'events-0-id': '',
            'events-0-DELETE': '',

            'events-1-event_type': event_type2.pk,
            'events-1-date': '2021-01-24',
            'events-1-id': '',
            'events-1-DELETE': '',
        }
