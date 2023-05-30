import json
import os

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

    def test_contribution_schema(self):
        filename = os.path.join(os.path.dirname(__file__), 'data',
                                'json_schema_base_contribution_without_subtypes.json')
        with open(filename) as f:
            json_data = json.load(f)
        self.assertEqual(json_data, self.portal.contribution_json_schema)


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
