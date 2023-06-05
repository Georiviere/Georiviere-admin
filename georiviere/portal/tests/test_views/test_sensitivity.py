from django.test import TestCase
from django.urls import reverse

from geotrek.sensitivity.tests.factories import SensitiveAreaFactory


class SensitivityViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.sensitivity = SensitiveAreaFactory.create(published=True)

    def test_sensitivity_detail_geojson_structure(self):
        url = reverse('api_portal:sensitivities-detail',
                      kwargs={'pk': self.sensitivity.pk, 'lang': 'fr', 'format': 'geojson'})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

        self.assertSetEqual(set(response.json().keys()), {'geometry', 'properties', 'type'})

    def test_sensitivity_detail_json_structure(self):
        url = reverse('api_portal:sensitivities-detail',
                      kwargs={'pk': self.sensitivity.pk, 'lang': 'fr'})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

        self.assertSetEqual(set(response.json().keys()), {'id', 'name', 'description', 'attachments', 'species'})

    def test_sensitivity_list_json_structure(self):
        url = reverse('api_portal:sensitivities-list',
                      kwargs={'lang': 'fr'})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

        self.assertSetEqual(set(response.json()[0].keys()), {'id', 'name', 'description', 'attachments', 'species'})

    def test_sensitivity_list_geojson_structure(self):
        url = reverse('api_portal:sensitivities-list',
                      kwargs={'lang': 'fr', 'format': 'geojson'})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

        self.assertSetEqual(set(response.json().keys()), {'type', 'features'})
