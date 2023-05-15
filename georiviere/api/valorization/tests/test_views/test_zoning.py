from django.test import TestCase
from django.urls import reverse

from georiviere.watershed.tests.factories import WatershedFactory

from geotrek.zoning.tests.factories import CityFactory, DistrictFactory


class WatershedViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.watershed = WatershedFactory.create()

    def test_watershed_detail_geojson_structure(self):
        url = reverse('api_valorization:watersheds-detail',
                      kwargs={'pk': self.watershed.pk, 'lang': 'fr', 'format': 'geojson'})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

        self.assertSetEqual(set(response.json().keys()), {'geometry', 'properties', 'type'})

    def test_watershed_list_geojson_structure(self):
        url = reverse('api_valorization:watersheds-list',
                      kwargs={'lang': 'fr', 'format': 'geojson'})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

        self.assertSetEqual(set(response.json().keys()), {'features', 'type'})

    def test_watershed_detail_json(self):
        url = reverse('api_valorization:watersheds-detail',
                      kwargs={'pk': self.watershed.pk, 'lang': 'fr', 'format': 'json'})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_watershed_list_json(self):
        url = reverse('api_valorization:watersheds-list',
                      kwargs={'lang': 'fr', 'format': 'json'})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)


class CityViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.city = CityFactory.create()

    def test_city_detail_geojson_structure(self):
        url = reverse('api_valorization:cities-detail',
                      kwargs={'pk': self.city.pk, 'lang': 'fr', 'format': 'geojson'})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

        self.assertSetEqual(set(response.json().keys()), {'geometry', 'properties', 'type'})

    def test_city_list_geojson_structure(self):
        url = reverse('api_valorization:cities-list',
                      kwargs={'lang': 'fr', 'format': 'geojson'})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

        self.assertSetEqual(set(response.json().keys()), {'features', 'type'})

    def test_city_detail_json(self):
        url = reverse('api_valorization:cities-detail',
                      kwargs={'pk': self.city.pk, 'lang': 'fr', 'format': 'json'})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_city_list_json(self):
        url = reverse('api_valorization:cities-list',
                      kwargs={'lang': 'fr', 'format': 'json'})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)


class DistrictViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.district = DistrictFactory.create()

    def test_district_detail_geojson_structure(self):
        url = reverse('api_valorization:districts-detail',
                      kwargs={'pk': self.district.pk, 'lang': 'fr', 'format': 'geojson'})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

        self.assertSetEqual(set(response.json().keys()), {'geometry', 'properties', 'type'})

    def test_district_list_geojson_structure(self):
        url = reverse('api_valorization:districts-list',
                      kwargs={'lang': 'fr', 'format': 'geojson'})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

        self.assertSetEqual(set(response.json().keys()), {'features', 'type'})

    def test_district_detail_json(self):
        url = reverse('api_valorization:districts-detail',
                      kwargs={'pk': self.district.pk, 'lang': 'fr', 'format': 'json'})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_city_list_json(self):
        url = reverse('api_valorization:districts-list',
                      kwargs={'lang': 'fr', 'format': 'json'})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)
