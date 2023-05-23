from django.test import TestCase
from django.urls import reverse

from geotrek.sensitivity.tests.factories import SensitiveAreaFactory


class SensitivityViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.sensitivity = SensitiveAreaFactory.create()

    def test_sensitivity_detail_geojson_structure(self):
        url = reverse('api_portal:sensitivities-detail',
                      kwargs={'pk': self.sensitivity.pk, 'lang': 'fr', 'format': 'geojson'})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

        self.assertSetEqual(set(response.json().keys()), {'geometry', 'properties', 'type'})

    def test_watershed_list_geojson_structure(self):
        url = reverse('api_portal:sensitivities-list',
                      kwargs={'lang': 'fr', 'format': 'geojson'})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

        self.assertSetEqual(set(response.json().keys()), {'features', 'type'})

    def test_watershed_detail_json(self):
        url = reverse('api_portal:sensitivities-detail',
                      kwargs={'pk': self.sensitivity.pk, 'lang': 'fr', 'format': 'json'})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_watershed_list_json(self):
        url = reverse('api_portal:sensitivities-list',
                      kwargs={'lang': 'fr', 'format': 'json'})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)
