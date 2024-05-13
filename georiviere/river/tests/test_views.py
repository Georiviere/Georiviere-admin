import os
from mapentity.tests.factories import SuperUserFactory
from unittest import mock

from django.conf import settings
from django.contrib.gis.geos import GEOSGeometry, Point, MultiPolygon, Polygon
from django.test import override_settings, TestCase
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from tempfile import TemporaryDirectory

from geotrek.authent.tests.factories import StructureFactory, UserFactory
from geotrek.zoning.tests.factories import CityFactory, DistrictFactory, RestrictedAreaFactory

from georiviere.tests import CommonRiverTest
from georiviere.description.tests.factories import StatusOnStreamFactory, StatusTypeFactory, StatusFactory, UsageFactory
from georiviere.description.models import Morphology, Status
from georiviere.knowledge.tests.factories import FollowUpKnowledgeFactory, FollowUpFactory, KnowledgeFactory
from georiviere.maintenance.tests.factories import InterventionFactory
from georiviere.studies.tests.factories import StudyFactory
from georiviere.river.models import Stream
from georiviere.river.tests.factories import StreamFactory, TopologyFactory
from georiviere.watershed.tests.factories import WatershedFactory


@override_settings(MEDIA_ROOT=TemporaryDirectory().name)
class StreamViewTestCase(CommonRiverTest):
    model = Stream
    modelfactory = StreamFactory

    def get_expected_json_attrs(self):
        return {
            'id': self.obj.pk,
            'structure': self.obj.structure.pk,
            'data_source': None,
            'geom_3d': self.obj.geom_3d.ewkt,
            'date_update': '2020-03-17T00:00:00Z',
            'date_insert': '2020-03-17T00:00:00Z',
            'length': self.obj.length,
            'ascent': self.obj.ascent,
            'descent': self.obj.descent,
            'flow': self.obj.flow,
            'min_elevation': self.obj.min_elevation,
            'max_elevation': self.obj.max_elevation,
            'slope': self.obj.slope,
            'source_location': self.obj.source_location.ewkt,
            'classification_water_policy': self.obj.classification_water_policy.pk,
            'name': self.obj.name,
            'description': self.obj.description,
            'geom': self.obj.geom.ewkt,
            'portals': []
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

    @override_settings(ICON_SIZES={'river_source': 18})
    def test_icon_size_source_location(self):
        """
        Check icon_sizes method in detail view
        """
        self.login()

        obj = self.modelfactory()

        response = self.client.get(obj.get_detail_url())
        self.assertContains(response, "iconSize: [18, 18]")

    def test_create_stream_default_source_location(self):
        """
        Check if source_location is set on stream creation
        """
        self.login()

        self.client.post(self._get_add_url(), self.get_good_data())
        stream = self.model.objects.last()
        self.assertEqual(stream.source_location.coords, stream.geom[0])

    def test_update_stream_source_location_unmodified(self):
        """
        Check if source_location is not modified on stream update
        """
        self.login()

        self.client.post(self._get_add_url(), self.get_good_data())
        stream = self.model.objects.last()
        self.assertEqual(stream.source_location.coords, stream.geom[0])

        # Set source_location using geom last point, then check if it's not modified on form update
        new_source_location = Point(stream.geom[-1][0], stream.geom[-1][1], srid=2154)
        stream.source_location = new_source_location
        stream.save()
        self._post_update_form(stream)
        self.assertNotEqual(stream.source_location.coords, stream.geom[0])
        self.assertEqual(stream.source_location.coords, new_source_location.coords)

    def test_create_stream_with_source_location(self):
        """
        Check if source_location is unmodified on stream creation if it is set
        """
        self.login()

        stream_data = self.get_good_data()
        point_data = Point(400000, 6000000, srid=2154)
        stream_data['source_location'] = point_data.ewkt
        self.client.post(self._get_add_url(), stream_data)
        stream = self.model.objects.last()
        self.assertNotEqual(stream.source_location.coords, stream.geom[0])
        self.assertEqual(stream.source_location.coords, point_data.coords)


class CutTopologyTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = UserFactory()

    def setUp(self):
        self.client.force_login(self.user)

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

    def test_cannot_cut_topology_locatepoint_beginning(self):
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

    def test_cannot_cut_topology_locatepoint_ending(self):
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


class DistanceToSourceTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = UserFactory()

    def setUp(self):
        self.client.force_login(self.user)

    def test_distance_to_source(self):
        geom = GEOSGeometry('SRID=4326;POINT(3 40)')
        geom_stream = GEOSGeometry('SRID=4326;LINESTRING(3 40, 2 40, 1 40)')
        geom_source_point = GEOSGeometry('SRID=4326;POINT(0 40)')
        geom_source_point_2154 = geom_source_point.transform(2154, clone=True)
        geom_stream_2154 = geom_stream.transform(2154, clone=True)
        StreamFactory.create(geom=geom_stream_2154,
                             source_location=geom_source_point_2154)
        response = self.client.get(reverse('river:distance_to_source'),
                                   data={'lng_distance': geom.coords[0],
                                         'lat_distance': geom.coords[1]})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {'distance': 257535.0})


class StreamDocumentReportTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.super_user = SuperUserFactory()
        cls.user = UserFactory()
        cls.stream = StreamFactory.create()
        cls.morphology = Morphology.objects.get()
        cls.status = Status.objects.get()
        cls.status.topology.start_position = 0
        cls.status.topology.end_position = 0.5
        cls.status.topology.save()
        cls.status_without_type = StatusFactory.create(topology=TopologyFactory.create(start_position=0.5,
                                                                                       end_position=0.75,
                                                                                       stream=cls.stream))
        cls.status_multi_types = StatusFactory.create(
            topology=TopologyFactory.create(start_position=0.75, end_position=1,
                                            stream=cls.stream))
        cls.status_type = StatusTypeFactory.create()
        cls.status_type_2 = StatusTypeFactory.create()
        cls.status.status_types.add(cls.status_type)
        cls.status_multi_types.status_types.add(cls.status_type)
        cls.status_multi_types.status_types.add(cls.status_type_2)

        cls.knowledge = KnowledgeFactory.create(geom=cls.stream.geom)

        # ZONING informations
        CityFactory.create(geom=MultiPolygon(Polygon.from_bbox(cls.stream.geom.extent)))
        DistrictFactory.create(geom=MultiPolygon(Polygon.from_bbox(cls.stream.geom.extent)))
        RestrictedAreaFactory.create(geom=MultiPolygon(Polygon.from_bbox(cls.stream.geom.extent)))

        WatershedFactory.create(geom=MultiPolygon(Polygon.from_bbox(cls.stream.geom.extent)))

    @mock.patch('georiviere.river.models.Stream.prepare_map_image_with_other_objects')
    @mock.patch('mapentity.models.MapEntityMixin.prepare_map_image')
    def test_document_report_stream_succeed(self, mock_prepare_map_image, mocked_prepare_map_image_wo):
        self.client.force_login(self.super_user)
        response = self.client.get(reverse('river:stream_printable', kwargs={'lang': "fr",
                                                                             'pk': self.stream.pk,
                                                                             'slug': self.stream.slug}))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response,
                                template_name='river/stream_report_pdf.html')
        self.assertEqual(response.context['status_types'][self.status_type.label]['percentage'], 75.0)
        self.assertEqual(response.context['status_types'][self.status_type_2.label]['percentage'], 25.0)
        self.assertEqual(os.path.join(settings.MEDIA_ROOT, 'maps', f'stream-{self.stream.pk}-usages.png'),
                         response.context['map_path_usage'])
        self.assertEqual(os.path.join(settings.MEDIA_ROOT, 'maps', f'stream-{self.stream.pk}-studies.png'),
                         response.context['map_path_study'])
        self.assertEqual(os.path.join(settings.MEDIA_ROOT, 'maps', f'stream-{self.stream.pk}-followups.png'),
                         response.context['map_path_other_followups'])
        self.assertEqual(os.path.join(settings.MEDIA_ROOT, 'maps', f'stream-{self.stream.pk}-interventions.png'),
                         response.context['map_path_other_interventions'])
        self.assertEqual(os.path.join(settings.MEDIA_ROOT, 'maps', f'knowledge-{self.knowledge.pk}.png'),
                         response.context['map_path_knowledge'][self.knowledge.pk])

    @mock.patch('georiviere.river.models.Stream.prepare_map_image_with_other_objects')
    @mock.patch('mapentity.models.MapEntityMixin.prepare_map_image')
    def test_document_report_stream_failed_no_permissions(self, mock_prepare_map_image, mocked_prepare_map_image_wo):
        self.client.force_login(self.user)
        response = self.client.get(reverse('river:stream_printable', kwargs={'lang': "fr",
                                                                             'pk': self.stream.pk,
                                                                             'slug': self.stream.slug}))
        self.assertEqual(response.status_code, 403)

    @mock.patch('georiviere.river.models.Stream.prepare_map_image_with_other_objects')
    @mock.patch('mapentity.models.MapEntityMixin.prepare_map_image')
    def test_document_report_stream_failed_not_authenticated(self, mock_prepare_map_image, mocked_prepare_map_image_wo):
        response = self.client.get(reverse('river:stream_printable', kwargs={'lang': "fr",
                                                                             'pk': self.stream.pk,
                                                                             'slug': self.stream.slug}))
        self.assertEqual(response.status_code, 403)


class APIStreamViewTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.super_user = SuperUserFactory()
        cls.stream = StreamFactory.create()
        cls.knowledge = FollowUpKnowledgeFactory.create_batch(1, geom=cls.stream.geom)
        cls.followup = FollowUpFactory.create()
        cls.followup_no_knowledge = FollowUpFactory.create_batch(2, geom=cls.stream.geom)
        cls.intervention = InterventionFactory.create_batch(2, geom=cls.stream.geom)
        cls.usage = UsageFactory.create_batch(3, geom=cls.stream.geom)
        cls.study = StudyFactory.create_batch(4, geom=cls.stream.geom)

    def setUp(self):
        self.client.force_login(self.super_user)

    def test_api_stream_list(self):
        response = self.client.get(reverse('river:stream-list'))
        self.assertEqual(len(response.json()), 1)

    def test_api_stream_followups_no_knowledges(self):
        response = self.client.get(reverse('river:stream-followups-no-knowledges',
                                           kwargs={'lang': 'fr',
                                                   'pk': self.stream.pk}))
        self.assertEqual(len(response.json()), 2)

    def test_api_stream_followups_no_knowledges_geojson(self):
        response = self.client.get(reverse('river:stream-followups-no-knowledges',
                                           kwargs={'lang': 'fr',
                                                   'pk': self.stream.pk,
                                                   'format': 'geojson'}))
        self.assertEqual(len(response.json()), 2)

    def test_api_stream_interventions_no_knowledges(self):
        response = self.client.get(reverse('river:stream-interventions-no-knowledges',
                                           kwargs={'lang': 'fr',
                                                   'pk': self.stream.pk}))
        self.assertEqual(len(response.json()), 2)

    def test_api_stream_interventions_no_knowledges_geojson(self):
        response = self.client.get(reverse('river:stream-interventions-no-knowledges',
                                           kwargs={'lang': 'fr',
                                                   'pk': self.stream.pk,
                                                   'format': 'geojson'}))
        self.assertEqual(len(response.json()['features']), 2)

    def test_api_stream_usages(self):
        response = self.client.get(reverse('river:stream-usages',
                                           kwargs={'lang': 'fr',
                                                   'pk': self.stream.pk}))
        self.assertEqual(len(response.json()), 3)

    def test_api_stream_usages_geojson(self):
        response = self.client.get(reverse('river:stream-usages',
                                           kwargs={'lang': 'fr',
                                                   'pk': self.stream.pk,
                                                   'format': 'geojson'}))
        self.assertEqual(len(response.json()['features']), 3)

    def test_api_stream_studies(self):
        response = self.client.get(reverse('river:stream-studies',
                                           kwargs={'lang': 'fr',
                                                   'pk': self.stream.pk}))
        self.assertEqual(len(response.json()), 4)

    def test_api_stream_studies_geojson(self):
        response = self.client.get(reverse('river:stream-studies',
                                           kwargs={'lang': 'fr',
                                                   'pk': self.stream.pk,
                                                   'format': 'geojson'}))
        self.assertEqual(len(response.json()['features']), 4)
