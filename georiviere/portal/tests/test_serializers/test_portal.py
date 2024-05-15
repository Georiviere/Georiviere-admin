from django.test import TestCase

from georiviere.flatpages.tests.factories import FlatPageFactory
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
        cls.portal_flatpages = PortalFactory.create()
        cls.portal_without_se = PortalFactory.create(spatial_extent=None)

        cls.flatpage_html = FlatPageFactory.create(content='test')
        cls.flatpage_html.portals.add(cls.portal_flatpages)

        cls.flatpage_link = FlatPageFactory.create(external_url='http://test.test')
        cls.flatpage_link.portals.add(cls.portal_flatpages)

        cls.serializer_portal = PortalSerializer(instance=cls.portal)
        cls.serializer_portal_layers_all_group = PortalSerializer(instance=cls.portal_layers_all_grouped)
        cls.serializer_portal_without_spatial_extent = PortalSerializer(instance=cls.portal_without_se)
        cls.serializer_portal_with_flatpages = PortalSerializer(instance=cls.portal_flatpages,
                                                                context={'portal_pk': cls.portal_flatpages.pk})
        watershed_portal = cls.portal.layers.get(layer_type='watersheds')
        watershed_portal.hidden = True
        watershed_portal.save()
        watershed_portal_all_grouped = cls.portal_layers_all_grouped.layers.get(layer_type='watersheds')
        watershed_portal_all_grouped.hidden = True
        watershed_portal_all_grouped.save()

    def test_portal_content(self):
        data = self.serializer_portal.data
        self.assertSetEqual(set(data.keys()), {'id', 'map', 'name', 'flatpages', 'title', 'description', 'extent',
                                               'max_zoom', 'min_zoom', 'main_color'})
        self.assertEqual(len(data['map']['group'][0]['layers']), 7)

    def test_portal_all_layers_grouped_content(self):
        data = self.serializer_portal_layers_all_group.data
        self.assertEqual(len(data['map']['group']), 1)
        self.assertEqual(data['map']['group'][0]['label'], 'Bar')
        self.assertSetEqual(set(data.keys()), {'id', 'map', 'name', 'flatpages', 'title', 'description', 'extent',
                                               'max_zoom', 'min_zoom', 'main_color'})
        self.assertEqual(len(data['map']['group'][0]['layers']), 7)

    def test_portal_without_se_content(self):
        data = self.serializer_portal_without_spatial_extent.data
        self.assertSetEqual(set(data.keys()), {'id', 'map', 'name', 'flatpages', 'title', 'description', 'extent',
                                               'max_zoom', 'min_zoom', 'main_color'})
        self.assertAlmostEqual(data['map']['bounds'][0], -5.5006, delta=4)
        self.assertAlmostEqual(data['map']['bounds'][3], 51.314, delta=4)

    def test_portal_with_flatpages_content(self):
        data = self.serializer_portal_with_flatpages.data
        self.assertSetEqual(set(data.keys()), {'id', 'map', 'name', 'flatpages', 'title', 'description', 'extent',
                                               'max_zoom', 'min_zoom', 'main_color'})
        self.assertEqual(set(data['flatpages'][0]), {'order', 'url', 'title', 'hidden'})
