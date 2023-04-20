from django.contrib.gis.geos import LineString
from django.test import TestCase

from georiviere.portal.tests.factories import PortalFactory
from georiviere.river.filters import StreamFilterSet
from georiviere.river.tests.factories import StreamFactory


class ZoningFilterTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.stream = StreamFactory.create(
            geom=LineString((10000, 10000), (50000, 50000)),
        )
        cls.portal_1 = PortalFactory.create(name="portal_1")
        cls.stream.portals.add(cls.portal_1)
        cls.portal_2 = PortalFactory.create(name="portal_2")

    def test_filter_portals(self):
        filter = StreamFilterSet(data={'portals': [self.portal_1, ]})

        self.assertIn(self.stream, filter.qs)
        self.assertEqual(len(filter.qs), 1)

        filter = StreamFilterSet(data={'portals': [self.portal_2, ]})

        self.assertEqual(len(filter.qs), 0)
