from django.test import TestCase

from . import factories

from georiviere.portal.models import MapLayer

from georiviere.valorization.tests.factories import POICategoryFactory


class PortalTest(TestCase):
    def test_create_portal(self):
        self.assertEqual(0, MapLayer.objects.count())
        factories.PortalFactory.create()
        self.assertEqual(8, MapLayer.objects.count())

    def test_create_portal_poi_category(self):
        POICategoryFactory.create()
        self.assertEqual(0, MapLayer.objects.count())
        factories.PortalFactory.create()
        self.assertEqual(9, MapLayer.objects.count())

        category = POICategoryFactory.create(label="New category")
        self.assertEqual(10, MapLayer.objects.count())

        category.delete()

        self.assertEqual(9, MapLayer.objects.count())
