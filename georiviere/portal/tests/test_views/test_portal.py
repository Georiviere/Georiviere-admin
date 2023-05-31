from django.test import TestCase
from django.urls import reverse

from georiviere.flatpages.tests.factories import FlatPageFactory
from georiviere.portal.tests.factories import PortalFactory


class PortalViewDetailTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.portal = PortalFactory.create()
        cls.flatpage_html = FlatPageFactory.create(content='test')
        cls.flatpage_html.portals.add(cls.portal)

    def test_portal_structure(self):
        url = reverse('api_portal:portal-detail', kwargs={'pk': self.portal.pk, 'lang': 'fr', 'format': 'json'})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

        self.assertEqual(list(response.json().keys()), ['id', 'name', 'map', 'flatpages'])
        self.assertEqual(len(response.json()['map']['group']), 1)
        self.assertEqual(response.json()['map']['group'][0]['label'], None)
