from django.test import TestCase
from django.urls import reverse

from georiviere.flatpages.tests.factories import FlatPageFactory
from georiviere.portal.tests.factories import PortalFactory


class FlatpageViewDetailTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.portal = PortalFactory.create()
        cls.flatpage = FlatPageFactory.create()
        cls.flatpage.portals.add(cls.portal)

    def test_flatpage_structure(self):
        url = reverse('api_portal:flatpages-detail', kwargs={'portal_pk': self.portal.pk,
                                                             'lang': 'fr',
                                                             'format': 'json',
                                                             'pk': self.flatpage.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

        self.assertEqual(list(response.json().keys()), ['title', 'content', 'pictures'])
