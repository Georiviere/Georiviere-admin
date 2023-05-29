from django.test import TestCase
from django.urls import reverse

from georiviere.contribution.models import Contribution, ContributionLandscapeElements
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

        self.assertSetEqual(set(response.json().keys()), {'type', 'required', 'properties', 'allOf'})

    def test_contribution_landscape_element(self):
        url = reverse('api_portal:contributions-list',
                      kwargs={'portal_pk': self.portal.pk, 'lang': 'fr'})
        response = self.client.post(url, data={"geom": "POINT(0 0)",
                                               "properties": '{"email_author": "x@x.x",  "date_observation": "2022-08-16", '
                                                             '"category": "Contribution Landscape Element",'
                                                             '"type": "Sinkhole"}'})
        self.assertEqual(response.status_code, 201)
        self.assertEqual(ContributionLandscapeElements.objects.count(), 1)
        contribution = Contribution.objects.first()
        landscape_element = contribution.landscape_element
        self.assertEqual(contribution.email_author, 'x@x.x')
        self.assertEqual(landscape_element.get_type_display(), 'Sinkhole')
