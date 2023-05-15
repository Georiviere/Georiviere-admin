from django.test import TestCase

from georiviere.portal.tests.factories import PortalFactory
from georiviere.valorization.tests.factories import POICategoryFactory
from georiviere.api.valorization.serializers.map import (MapBaseLayerSerializer, MapLayerSerializer,
                                                         MapGroupLayerSerializer)


class MapSerializerTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.portal = PortalFactory.create()
        cls.serializer_layer = MapLayerSerializer(instance=cls.portal.layers.first())
        cls.serializer_base_layer = MapBaseLayerSerializer(instance=cls.portal.map_base_layers.first())
        cls.serializer_group_layer = MapGroupLayerSerializer(instance=cls.portal.mapgrouplayer_set.first())

    def test_map_layer_content(self):
        data = self.serializer_layer.data
        self.assertSetEqual(set(data.keys()), {'url', 'label', 'id', 'options', 'default_active', 'geojson_url'})

    def test_map_layer_content_poi_categories(self):
        category = POICategoryFactory.create()
        data = MapLayerSerializer(instance=self.portal.layers.filter(layer_type__startswith='pois').first()).data

        self.assertSetEqual(set(data.keys()), {'url', 'label', 'id', 'options', 'default_active', 'geojson_url'})
        self.assertEqual(data['geojson_url'], f'{self.portal.pk}/pois/category/{category.pk}.geojson')

    def test_map_base_layer_content(self):
        data = self.serializer_base_layer.data
        self.assertSetEqual(set(data.keys()), {'id', 'url', 'control', 'label'})

    def test_map_group_layer_content(self):
        data = self.serializer_group_layer.data
        self.assertSetEqual(set(data.keys()), {'layers', 'label'})
