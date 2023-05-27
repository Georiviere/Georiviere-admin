from django.test import TestCase
from django.urls import reverse

from georiviere.portal.tests.factories import PortalFactory


class ContributionViewDetailTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.portal = PortalFactory.create()

    def test_contribution_structure(self):
        url = reverse('api_portal:contributions-contributions_schema',
                      kwargs={'portal_pk': self.portal.pk, 'lang': 'fr'})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

        self.assertEqual(list(response.json().keys()), ['type', 'required', 'properties', 'allOf'])
