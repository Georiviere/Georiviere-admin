from requests import Response
from unittest import mock

from django.conf import settings
from django.contrib.gis.geos import Point, LineString
from django.test import TestCase, RequestFactory

from georiviere.finances_administration.tests.factories import AdministrativeFileFactory
from georiviere.description.tests.factories import MorphologyFactory, StatusFactory, UsageFactory
from georiviere.river.models import DistanceToSource, Stream
from georiviere.river.tests.factories import TopologyFactory, StreamFactory, ClassificationWaterPolicyFactory


class StreamModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.stream = StreamFactory.create(
            geom=LineString((10000, 10000), (50000, 50000)),
        )

    def test_prepare_map_image_with_usages(self):
        rooturl = RequestFactory().get('/').build_absolute_uri('/')
        with mock.patch('mapentity.helpers.get_source') as mocked_source:
            def side_effect():
                response = Response()
                response.status_code = 200
                response._content = bytes(
                    "test",
                    'utf-8'
                )
                return response

            mocked_source.return_value = side_effect()
            self.assertTrue(self.stream.prepare_map_image_with_other_objects(rooturl, ['usages']))
            self.assertFalse(self.stream.prepare_map_image_with_other_objects(rooturl, ['usages']))

            UsageFactory.create(geom=self.stream.geom)

            self.assertTrue(self.stream.prepare_map_image_with_other_objects(rooturl, ['usages']))
            self.assertFalse(self.stream.prepare_map_image_with_other_objects(rooturl, ['usages']))

            self.stream.name = "New name"
            self.stream.save()

            self.assertTrue(self.stream.prepare_map_image_with_other_objects(rooturl, ['usages']))


class ClassificationWaterPolicyModelTest(TestCase):
    def test_str(self):
        classification = ClassificationWaterPolicyFactory.create()
        self.assertEqual(str(classification), classification.label)


class TopologyTest(TestCase):

    def test_str(self):
        morphology = MorphologyFactory.create()
        status = StatusFactory.create()
        lonely_topology = TopologyFactory()
        self.assertEqual(str(status.topology), "Status {}".format(str(status)))
        self.assertEqual(str(morphology.topology), "Morphology {}".format(str(morphology)))
        self.assertEqual(str(lonely_topology), "Topology {}".format(lonely_topology.pk))


class StreamSourceLocationTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.stream1 = StreamFactory.create(
            geom=LineString((10000, 10000), (50000, 50000)),
        )
        cls.stream2 = StreamFactory.create(
            geom=LineString((10000, 10000), (50000, 50000)),
            source_location=Point(0, 0, srid=settings.SRID),
        )
        cls.usage_point = UsageFactory.create(
            geom=Point(10000, 10020)
        )
        cls.administrative_file = AdministrativeFileFactory.create()

    def test_source_location_default(self):
        """Test if source_location is set on save()"""
        self.assertAlmostEqual(self.stream1.source_location.coords, (10000, 10000))

    def test_get_map_image_extent(self):
        """Test get_map_image_extent method with source location not in bbox"""
        lng_min, lat_min, lng_max, lat_max = self.stream2.get_map_image_extent()
        self.assertAlmostEqual(lng_min, -1.363081210117898)
        self.assertAlmostEqual(lat_min, -5.9838563092087576)
        self.assertAlmostEqual(lng_max, -1.0680441780204335)
        self.assertAlmostEqual(lat_max, -5.655019875165679)

    def test_distance_to_source(self):
        """Test distance from a given object to stream source according to different geom"""
        self.assertAlmostEqual(self.stream1.distance_to_source(self.usage_point), 28.2842712)
        self.assertEqual(self.stream1.distance_to_source(self.administrative_file), None)
        self.assertEqual(DistanceToSource.objects.count(), 2)
        usage_point = UsageFactory.create(
            geom=Point(10000, 10010)
        )
        self.assertEqual(DistanceToSource.objects.count(), 4)
        usage_point.delete()
        self.assertEqual(DistanceToSource.objects.count(), 2)


class SnapTest(TestCase):
    def test_snap_not_saved(self):
        p = Stream()
        with self.assertRaisesRegex(ValueError, "Cannot compute snap on unsaved stream"):
            p.snap(Point(0, 0))

    def test_snap_reproj(self):
        p = StreamFactory.create(geom=LineString(Point(700000, 6600000), Point(700100, 6600100), srid=settings.SRID))
        snap = p.snap(Point(3, 46.5, srid=4326))
        self.assertEqual(snap.x, 700000)
        self.assertEqual(snap.y, 6600000)
