from django.test import TestCase
from django.urls import reverse

from georiviere.portal.tests.factories import PortalFactory


class PortalViewDetailTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.portal = PortalFactory.create()

    def test_portal_structure(self):
        url = reverse('api_portal:portal-detail', kwargs={'pk': self.portal.pk, 'lang': 'fr', 'format': 'json'})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

        self.assertEqual(list(response.json().keys()), ['id', 'name', 'map', 'group', 'spatialExtent'])
        self.assertEqual(len(response.json()['group']), 1)
        self.assertEqual(response.json()['group'][0]['label'], None)
