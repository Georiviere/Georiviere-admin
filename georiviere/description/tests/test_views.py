from tempfile import TemporaryDirectory

from django.test import override_settings
from django.utils.translation import gettext_lazy as _
from geotrek.authent.tests.factories import StructureFactory

from georiviere.river.tests import TopologyTestCase
from georiviere.river.tests.factories import StreamFactory
from georiviere.tests import CommonRiverTest
from .factories import LandFactory, LandTypeFactory, UsageFactory, UsageTypeFactory, StatusTypeFactory, \
    StatusOnStreamFactory, MorphologyOnStreamFactory, PlanLayoutTypeFactory, ControlTypeFactory

from ..models import Land, Morphology, Status, Usage


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
            'land_type': self.obj.land_type.pk,
            'control_type': self.obj.control_type.pk
        }

    def get_bad_data(self):
        return {'geom': '{"geom": "LINESTRING (0.0 0.0, 1.0 1.0)"}'}, _("Geometry invalid snapping.")

    def get_good_data(self):
        structure = StructureFactory.create()
        land_type = LandTypeFactory.create()
        control_type = ControlTypeFactory.create()
        temp_data = self.modelfactory.build(structure=structure)
        return {
            'structure': structure.pk,
            'geom': '{"geom": "%s", "snap": [%s]}' % (temp_data.geom.transform(4326, clone=True).ewkt,
                                                      ','.join(['null'] * len(temp_data.geom.coords))),
            'land_type': land_type.pk,
            'control_type': control_type.pk,
            'owner': temp_data.owner,
            'description': temp_data.description
        }


@override_settings(MEDIA_ROOT=TemporaryDirectory().name)
class UsageViewTestCase(CommonRiverTest):
    model = Usage
    modelfactory = UsageFactory

    def get_bad_data(self):
        return {'geom': '{"geom": "LINESTRING (0.0 0.0, 1.0 1.0)"}'}, _("Geometry invalid snapping.")

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
            'geom': '{"geom": "%s", "snap": [%s]}' % (temp_data.geom.transform(4326, clone=True).ewkt,
                                                      ','.join(['null'] * len(temp_data.geom.coords))),
            'usage_types': [usage_type.pk, ]
        }


@override_settings(MEDIA_ROOT=TemporaryDirectory().name)
class SatusViewTestCase(TopologyTestCase):
    model = Status
    modelfactory = StatusOnStreamFactory

    def get_expected_json_attrs(self):
        return {
            'id': self.obj.pk,
            'date_update': self.obj.date_update.isoformat().replace('+00:00', 'Z'),
            'date_insert': self.obj.date_insert.isoformat().replace('+00:00', 'Z'),
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


@override_settings(MEDIA_ROOT=TemporaryDirectory().name)
class MorphologyViewTestCase(TopologyTestCase):
    model = Morphology
    modelfactory = MorphologyOnStreamFactory

    def get_expected_json_attrs(self):
        return {
            'id': self.obj.pk,
            'date_update': self.obj.date_update.isoformat().replace('+00:00', 'Z'),
            'date_insert': self.obj.date_insert.isoformat().replace('+00:00', 'Z'),
            'description': '',
            'bank_state_left': None,
            'bank_state_right': None,
            'full_edge_height': 0.0,
            'full_edge_width': 0.0,
            'facies_diversity': None,
            'good_working_space_left': None,
            'good_working_space_right': None,
            'granulometric_diversity': None,
            'habitats_diversity': None,
            'main_flow': None,
            'main_habitat': None,
            'secondary_flows': [],
            'secondary_habitats': [],
            'sediment_dynamic': None,
            'plan_layout': None,
            'length': self.obj.length,
            'geom_3d': self.obj.geom_3d.ewkt,
            'ascent': self.obj.ascent,
            'descent': self.obj.descent,
            'min_elevation': self.obj.min_elevation,
            'max_elevation': self.obj.max_elevation,
            'slope': self.obj.slope,
            'geom': self.obj.geom.ewkt,
            'topology': self.obj.topology.pk,
        }

    def get_good_data(self):
        structure = StructureFactory.create()
        plan_layout = PlanLayoutTypeFactory.create()
        stream = StreamFactory.create()

        topology = stream.topologies.filter(morphology__isnull=False).get()
        temp_data = self.modelfactory.build(structure=structure)
        return {
            'geom': temp_data.geom.ewkt,
            'plan_layout': plan_layout.pk,
            'topology': topology.pk,
        }

    def _check_update_geom_permission(self, response):
        self.assertIn(b'.modifiable = false;', response.content)
