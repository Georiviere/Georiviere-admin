from django.conf import settings
from django.contrib.gis.geos import Point, LineString
from django.test import TestCase

from geotrek.authent.factories import StructureFactory, UserFactory

from georiviere.description.tests.factories import MorphologyFactory, StatusFactory
from georiviere.river.tests.factories import TopologyFactory, StreamFactory

class TopologyTest(TestCase):

    def test_str(self):
        morphology = MorphologyFactory.create()
        status = StatusFactory.create()
        lonely_topology = TopologyFactory()
        self.assertEqual(str(status.topology), "Status {}".format(status.pk))
        self.assertEqual(str(morphology.topology), "Morphology {}".format(morphology.pk))
        self.assertEqual(str(lonely_topology), "Topology {}".format(lonely_topology.pk))


class MapImageExtentTest(TestCase):
    def setUp(self):
        self.stream = StreamFactory.create(
            geom=LineString((10000, 10000), (50000, 50000)),
            source_location=Point(0, 0, srid=settings.SRID),
        )

    def test_get_map_image_extent(self):
        lng_min, lat_min, lng_max, lat_max = self.stream.get_map_image_extent()
        self.assertAlmostEqual(lng_min, -1.363081210117898)
        self.assertAlmostEqual(lat_min, -5.9838563092087576)
        self.assertAlmostEqual(lng_max, -1.0680441780204335)
        self.assertAlmostEqual(lat_max, -5.655019875165679)
