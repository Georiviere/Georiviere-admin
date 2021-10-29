from tempfile import TemporaryDirectory

from django.test import override_settings
from geotrek.authent.factories import StructureFactory

from georiviere.river.tests import TopologyTestCase
from georiviere.river.tests.factories import StreamFactory
from georiviere.tests import CommonRiverTest
from .factories import LandFactory, LandTypeFactory, UsageFactory, UsageTypeFactory, StatusTypeFactory, \
    StatusOnStreamFactory
from ..models import Land, Status, Usage


@override_settings(MEDIA_ROOT=TemporaryDirectory().name)
class LandViewTestCase(CommonRiverTest):
    model = Land
    modelfactory = LandFactory

    def get_expected_json_attrs(self):
        return {
            'id': self.obj.pk,
            'structure': self.obj.structure.pk,
            'agreement': self.obj.agreement,
            'identifier': self.obj.identifier,
            'date_update': '2020-03-17T00:00:00Z',
            'date_insert': '2020-03-17T00:00:00Z',
            'length': self.obj.length,
            'description': self.obj.description,
            'owner': self.obj.owner,
            'geom_3d': self.obj.geom_3d.ewkt,
            'ascent': self.obj.ascent,
            'descent': self.obj.descent,
            'min_elevation': self.obj.min_elevation,
            'max_elevation': self.obj.max_elevation,
            'slope': self.obj.slope,
            'geom': self.obj.geom.ewkt,
            'land_type': self.obj.land_type.pk
        }

    def get_good_data(self):
        structure = StructureFactory.create()
        land_type = LandTypeFactory.create()
        temp_data = self.modelfactory.build(structure=structure)
        return {
            'structure': structure.pk,
            'geom': temp_data.geom.ewkt,
            'land_type': land_type.pk,
            'owner': temp_data.owner,
            'description': temp_data.description
        }


@override_settings(MEDIA_ROOT=TemporaryDirectory().name)
class UsageViewTestCase(CommonRiverTest):
    model = Usage
    modelfactory = UsageFactory

    def get_expected_json_attrs(self):
        return {
            'id': self.obj.pk,
            'structure': self.obj.structure.pk,
            'date_update': '2020-03-17T00:00:00Z',
            'date_insert': '2020-03-17T00:00:00Z',
            'description': '',
            'length': self.obj.length,
            'geom_3d': self.obj.geom_3d.ewkt,
            'ascent': self.obj.ascent,
            'descent': self.obj.descent,
            'min_elevation': self.obj.min_elevation,
            'max_elevation': self.obj.max_elevation,
            'slope': self.obj.slope,
            'geom': self.obj.geom.ewkt,
            'usage_types': []
        }

    def get_good_data(self):
        structure = StructureFactory.create()
        usage_type = UsageTypeFactory.create()
        temp_data = self.modelfactory.build(structure=structure, usage_types=[usage_type])
        return {
            'structure': structure.pk,
            'geom': temp_data.geom.ewkt,
            'usage_types': [usage_type.pk, ]
        }


@override_settings(MEDIA_ROOT=TemporaryDirectory().name)
class SatusViewTestCase(TopologyTestCase):
    model = Status
    modelfactory = StatusOnStreamFactory

    def get_expected_json_attrs(self):
        return {
            'id': self.obj.pk,
            'date_update': '2020-03-17T00:00:00Z',
            'date_insert': '2020-03-17T00:00:00Z',
            'description': '',
            'length': self.obj.length,
            'geom_3d': self.obj.geom_3d.ewkt,
            'ascent': self.obj.ascent,
            'descent': self.obj.descent,
            'min_elevation': self.obj.min_elevation,
            'max_elevation': self.obj.max_elevation,
            'referencial': False,
            'regulation': False,
            'status_types': [],
            'slope': self.obj.slope,
            'geom': self.obj.geom.ewkt,
            'topology': self.obj.topology.pk,
        }

    def get_good_data(self):
        structure = StructureFactory.create()
        status_types = StatusTypeFactory.create()
        stream = StreamFactory.create()

        topology = stream.topologies.filter(status__isnull=True).get()
        temp_data = self.modelfactory.build(structure=structure)
        return {
            'geom': temp_data.geom.ewkt,
            'status_types': [status_types.pk],
            'topology': topology.pk,
        }

    def _check_update_geom_permission(self, response):
        self.assertIn(b'.modifiable = false;', response.content)
