from django.test import TestCase

from . import factories


class PortalTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.portal = factories.PortalFactory(
            name="Name portal",
        )

    def test_str(self):
        self.assertEqual(str(self.portal), "Name portal")


class MapBaseLayerTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.base_layer = factories.MapBaseLayerFactory(
            label="Base layer",
        )

    def test_str(self):
        self.assertEqual(str(self.base_layer), "Base layer")


class MapLayerTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.portal = factories.PortalFactory()
        cls.layer = cls.portal.layers.first()
        cls.layer.label = 'Other label'
        cls.layer.save()

    def test_str(self):
        self.assertEqual(str(self.layer), "Other label")


class GroupMapLayerTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.group = factories.GroupMapLayerFactory(label='Group')

    def test_str(self):
        self.assertEqual(str(self.group), "Group")
