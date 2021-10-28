from tempfile import TemporaryDirectory

from django.conf import settings
from django.contrib.gis.geos import GEOSGeometry
from django.test import override_settings, TestCase
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from geotrek.authent.factories import StructureFactory, UserFactory

from description.models import Status
from description.tests.factories import StatusOnStreamFactory
from georiviere.tests import CommonRiverTest
from river.models import Stream
from river.tests.factories import StreamFactory


@override_settings(MEDIA_ROOT=TemporaryDirectory().name)
class StreamViewTestCase(CommonRiverTest):
    model = Stream
    modelfactory = StreamFactory

    def get_expected_json_attrs(self):
        return {
            'id': self.obj.pk,
            'structure': self.obj.structure.pk,
            'geom_3d': self.obj.geom_3d.ewkt,
            'date_update': '2020-03-17T00:00:00Z',
            'date_insert': '2020-03-17T00:00:00Z',
            'length': self.obj.length,
            'ascent': self.obj.ascent,
            'descent': self.obj.descent,
            'min_elevation': self.obj.min_elevation,
            'max_elevation': self.obj.max_elevation,
            'slope': self.obj.slope,
            'name': self.obj.name,
            'geom': self.obj.geom.ewkt,
        }

    def get_bad_data(self):
        return {'geom': '{"geom": "LINESTRING (0.0 0.0, 1.0 1.0)"}'}, _("Linestring invalid snapping.")

    def get_good_data(self):
        structure = StructureFactory.create()
        temp_data = self.modelfactory.build(structure=structure)
        geom_transform = temp_data.geom.transform(settings.API_SRID, clone=True)
        return {
            'structure': structure.pk,
            'name': temp_data.name,
            'geom': '{"geom": "%s", "snap": [%s]}' % (geom_transform.ewkt,
                                                      ','.join(['null'] * len(geom_transform.coords))),
        }


class CutTopologyTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = UserFactory(password='booh')

    def setUp(self):
        self.client.login(username=self.user.username, password="booh")

    def test_cut_topology(self):
        geom = GEOSGeometry('SRID=4326;LINESTRING(3 40, 4 40, 5 40)')
        geom_2154 = geom.transform(2154, clone=True)
        obj = StatusOnStreamFactory.create(geom=geom_2154)
        self.assertEqual(Status.objects.count(), 1)
        response = self.client.post(reverse('river:cut_topology'),
                                    data={'topology': obj.topology.pk,
                                          'lng': geom.coords[1][0],
                                          'lat': geom.coords[1][1]})
        self.assertEqual(response.status_code, 302)
        obj.refresh_from_db()
        self.assertEqual(Status.objects.count(), 2)
        self.assertAlmostEqual(obj.geom.transform(4326, clone=True).coords[0][0], 4)

    def test_canot_cut_topology_locatepoint_beginning(self):
        geom = GEOSGeometry('SRID=4326;LINESTRING(3 40, 4 40, 5 40)')
        obj = StatusOnStreamFactory.create(geom=geom.transform(2154, clone=True))
        self.assertEqual(Status.objects.count(), 1)
        response = self.client.post(reverse('river:cut_topology'),
                                    data={'topology': obj.topology.pk,
                                          'lng': geom.coords[0][0],
                                          'lat': geom.coords[0][1]}, follow=True)
        # self.assertEqual(response.status_code, 302)
        obj.refresh_from_db()
        self.assertEqual(Status.objects.count(), 1)
        self.assertEqual(str([msg for msg in response.context['messages']][0]), 'Topology could not be cut')

    def test_canot_cut_topology_locatepoint_ending(self):
        geom = GEOSGeometry('SRID=4326;LINESTRING(3 40, 4 40, 5 40)')
        obj = StatusOnStreamFactory.create(geom=geom.transform(2154, clone=True))
        self.assertEqual(Status.objects.count(), 1)
        response = self.client.post(reverse('river:cut_topology'),
                                    data={'topology': obj.topology.pk,
                                          'lng': geom.coords[2][0],
                                          'lat': geom.coords[2][1]}, follow=True)
        # self.assertEqual(response.status_code, 302)
        obj.refresh_from_db()
        self.assertEqual(Status.objects.count(), 1)
        self.assertEqual(str([msg for msg in response.context['messages']][0]), 'Topology could not be cut')
