from django.conf import settings
from django.test import TestCase

from georiviere.portal.tests.factories import GroupMapLayerFactory, PortalFactory
from georiviere.portal.serializers.portal import PortalSerializer


class PortalSerializerTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.portal = PortalFactory.create()
        cls.portal_layers_all_grouped = PortalFactory.create()
        group_layer = GroupMapLayerFactory.create(portal=cls.portal_layers_all_grouped, label="Bar")
        for layer in cls.portal_layers_all_grouped.layers.all():
            layer.group_layer = group_layer
            layer.save()
        cls.portal_without_se = PortalFactory.create(spatial_extent=None)
        cls.serializer_portal = PortalSerializer(instance=cls.portal)
        cls.serializer_portal_layers_all_group = PortalSerializer(instance=cls.portal_layers_all_grouped)
        cls.serializer_portal_without_spatial_extent = PortalSerializer(instance=cls.portal_without_se)

    def test_portal_content(self):
        data = self.serializer_portal.data
        self.assertSetEqual(set(data.keys()), {'id', 'map', 'name', 'group', 'spatial_extent'})

    def test_portal_all_layers_grouped_content(self):
        data = self.serializer_portal_layers_all_group.data
        self.assertEqual(len(data['group']), 1)
        self.assertEqual(data['group'][0]['label'], 'Bar')
        self.assertSetEqual(set(data.keys()), {'id', 'map', 'name', 'group', 'spatial_extent'})

    def test_portal_without_se_content(self):
        data = self.serializer_portal_without_spatial_extent.data
        self.assertSetEqual(set(data.keys()), {'id', 'map', 'name', 'group', 'spatial_extent'})
        self.assertEqual(data['spatial_extent'], settings.SPATIAL_EXTENT)
