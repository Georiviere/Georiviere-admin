from django.test import TestCase
from django.urls import reverse

from georiviere.portal.tests.factories import PortalFactory
from georiviere.watershed.tests.factories import WatershedFactory, WatershedTypeFactory

from geotrek.zoning.tests.factories import CityFactory, DistrictFactory


class WatershedViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.portal = PortalFactory.create()
        watershed_type = WatershedTypeFactory.create()
        watershed_type.portals.add(cls.portal)
        cls.watershed = WatershedFactory.create(watershed_type=watershed_type)

    def test_watershed_detail_geojson_structure(self):
        url = reverse('api_portal:watersheds-detail',
                      kwargs={'portal_pk': self.portal.pk, 'pk': self.watershed.pk, 'lang': 'fr', 'format': 'geojson'})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

        self.assertSetEqual(set(response.json().keys()), {'geometry', 'properties', 'type'})

    def test_watershed_list_geojson_structure(self):
        url = reverse('api_portal:watersheds-list',
                      kwargs={'portal_pk': self.portal.pk, 'lang': 'fr', 'format': 'geojson'})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

        self.assertSetEqual(set(response.json().keys()), {'features', 'type'})

    def test_watershed_detail_json(self):
        url = reverse('api_portal:watersheds-detail',
                      kwargs={'portal_pk': self.portal.pk, 'pk': self.watershed.pk, 'lang': 'fr', 'format': 'json'})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

        self.assertSetEqual(set(response.json().keys()), {'id', 'type', 'name'})

    def test_watershed_list_json(self):
        url = reverse('api_portal:watersheds-list',
                      kwargs={'portal_pk': self.portal.pk, 'lang': 'fr', 'format': 'json'})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

        self.assertSetEqual(set(response.json()[0].keys()), {'id', 'name', 'type'})


class CityViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.city = CityFactory.create()

    def test_city_detail_geojson_structure(self):
        url = reverse('api_portal:cities-detail',
                      kwargs={'pk': self.city.pk, 'lang': 'fr', 'format': 'geojson'})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

        self.assertSetEqual(set(response.json().keys()), {'geometry', 'properties', 'type'})

    def test_city_list_geojson_structure(self):
        url = reverse('api_portal:cities-list',
                      kwargs={'lang': 'fr', 'format': 'geojson'})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

        self.assertSetEqual(set(response.json().keys()), {'features', 'type'})

    def test_city_detail_json(self):
        url = reverse('api_portal:cities-detail',
                      kwargs={'pk': self.city.pk, 'lang': 'fr', 'format': 'json'})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

        self.assertSetEqual(set(response.json().keys()), {'id', 'name'})

    def test_city_list_json(self):
        url = reverse('api_portal:cities-list',
                      kwargs={'lang': 'fr', 'format': 'json'})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

        self.assertSetEqual(set(response.json()[0].keys()), {'id', 'name'})


class DistrictViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.district = DistrictFactory.create()

    def test_district_detail_geojson_structure(self):
        url = reverse('api_portal:districts-detail',
                      kwargs={'pk': self.district.pk, 'lang': 'fr', 'format': 'geojson'})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

        self.assertSetEqual(set(response.json().keys()), {'geometry', 'properties', 'type'})

    def test_district_list_geojson_structure(self):
        url = reverse('api_portal:districts-list',
                      kwargs={'lang': 'fr', 'format': 'geojson'})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

        self.assertSetEqual(set(response.json().keys()), {'features', 'type'})

    def test_district_detail_json(self):
        url = reverse('api_portal:districts-detail',
                      kwargs={'pk': self.district.pk, 'lang': 'fr', 'format': 'json'})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

        self.assertSetEqual(set(response.json().keys()), {'id', 'name'})

    def test_district_list_json(self):
        url = reverse('api_portal:districts-list',
                      kwargs={'lang': 'fr', 'format': 'json'})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

        self.assertSetEqual(set(response.json()[0].keys()), {'id', 'name'})
