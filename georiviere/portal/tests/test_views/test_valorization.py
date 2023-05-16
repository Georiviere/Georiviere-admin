from django.test import TestCase
from django.urls import reverse

from georiviere.portal.tests.factories import PortalFactory
from georiviere.valorization.tests.factories import POIFactory


class POIViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.portal = PortalFactory.create()
        cls.poi = POIFactory.create()
        cls.poi.portals.add(cls.portal)

    def test_poi_detail_geojson_structure(self):
        url = reverse('api_portal:pois-detail',
                      kwargs={'portal_pk': self.portal.pk, 'pk': self.poi.pk, 'lang': 'fr', 'format': 'geojson'})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

        self.assertSetEqual(set(response.json().keys()), {'geometry', 'properties', 'type'})

    def test_poi_detail_json_structure(self):
        url = reverse('api_portal:pois-detail',
                      kwargs={'portal_pk': self.portal.pk, 'pk': self.poi.pk, 'lang': 'fr', 'format': 'json'})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertSetEqual(set(response.json().keys()), {'attachments', 'type', 'name', 'id', 'description'})

    def test_poi_list_geojson_structure(self):
        url = reverse('api_portal:pois-list',
                      kwargs={'portal_pk': self.portal.pk, 'lang': 'fr', 'format': 'geojson'})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertSetEqual(set(response.json().keys()), {'type', 'features'})

    def test_poi_list_json_structure(self):
        url = reverse('api_portal:pois-list',
                      kwargs={'portal_pk': self.portal.pk, 'lang': 'fr', 'format': 'json'})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()), 1)
        self.assertSetEqual(set(response.json()[0].keys()), {'attachments', 'type', 'name', 'id', 'description'})

    def test_poi_category_list_json_structure(self):
        url = reverse('api_portal:pois-category',
                      kwargs={'portal_pk': self.portal.pk, 'category_pk': self.poi.type.category.pk, 'lang': 'fr',
                              'format': 'json'})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()), 1)
        self.assertSetEqual(set(response.json()[0].keys()), {'attachments', 'name', 'type', 'id', 'description'})

    def test_poi_category_list_geojson_structure(self):
        url = reverse('api_portal:pois-category',
                      kwargs={'portal_pk': self.portal.pk, 'category_pk': self.poi.type.category.pk,
                              'lang': 'fr', 'format': 'geojson'})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertSetEqual(set(response.json().keys()), {'type', 'features'})
