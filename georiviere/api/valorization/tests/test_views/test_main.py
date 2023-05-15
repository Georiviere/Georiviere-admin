from django.test import TestCase
from django.urls import reverse


class VersionViewTest(TestCase):
    def test_version(self):
        url_version = reverse('api_valorization:version', kwargs={'lang': 'fr'})
        response = self.client.get(url_version)
        self.assertSetEqual(set(response.json().keys()), {'version'})
