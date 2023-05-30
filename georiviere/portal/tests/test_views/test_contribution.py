from django.test import TestCase
from django.urls import reverse
from unittest import mock

from georiviere.contribution.models import (Contribution, ContributionQuality, ContributionLandscapeElements,
                                            ContributionQuantity, ContributionFaunaFlora, ContributionPotentialDamage)
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
                                                             '"category": "Contribution Élément Paysagers",'
                                                             '"type": "Doline"}'})
        self.assertEqual(response.status_code, 201)
        self.assertEqual(ContributionLandscapeElements.objects.count(), 1)
        contribution = Contribution.objects.first()
        landscape_element = contribution.landscape_element
        self.assertEqual(contribution.email_author, 'x@x.x')
        self.assertEqual(landscape_element.get_type_display(), 'Doline')

    def test_contribution_quality(self):
        url = reverse('api_portal:contributions-list',
                      kwargs={'portal_pk': self.portal.pk, 'lang': 'fr'})
        response = self.client.post(url, data={"geom": "POINT(0 0)",
                                               "properties": '{"email_author": "x@x.x",  "date_observation": "2022-08-16", '
                                                             '"category": "Contribution Qualité",'
                                                             '"type": "Pollution"}'})
        self.assertEqual(response.status_code, 201)
        self.assertEqual(ContributionQuality.objects.count(), 1)
        contribution = Contribution.objects.first()
        quality = contribution.quality
        self.assertEqual(contribution.email_author, 'x@x.x')
        self.assertEqual(quality.get_type_display(), 'Pollution')

    def test_contribution_quantity(self):
        url = reverse('api_portal:contributions-list',
                      kwargs={'portal_pk': self.portal.pk, 'lang': 'fr'})
        response = self.client.post(url, data={"geom": "POINT(0 0)",
                                               "properties": '{"email_author": "x@x.x",  "date_observation": "2022-08-16", '
                                                             '"category": "Contribution Quantité",'
                                                             '"type": "A sec"}'})
        self.assertEqual(response.status_code, 201)
        self.assertEqual(ContributionQuantity.objects.count(), 1)
        contribution = Contribution.objects.first()
        quantity = contribution.quantity
        self.assertEqual(contribution.email_author, 'x@x.x')
        self.assertEqual(quantity.get_type_display(), 'A sec')

    def test_contribution_faunaflora(self):
        url = reverse('api_portal:contributions-list',
                      kwargs={'portal_pk': self.portal.pk, 'lang': 'fr'})
        response = self.client.post(url, data={"geom": "POINT(0 0)",
                                               "properties": '{"email_author": "x@x.x",  "date_observation": "2022-08-16", '
                                                             '"category": "Contribution Faune-Flore",'
                                                             '"type": "Espèce invasive"}'})
        self.assertEqual(response.status_code, 201)
        self.assertEqual(ContributionFaunaFlora.objects.count(), 1)
        contribution = Contribution.objects.first()
        fauna_flora = contribution.fauna_flora
        self.assertEqual(contribution.email_author, 'x@x.x')
        self.assertEqual(fauna_flora.get_type_display(), 'Espèce invasive')

    def test_contribution_potential_damages(self):
        url = reverse('api_portal:contributions-list',
                      kwargs={'portal_pk': self.portal.pk, 'lang': 'fr'})
        response = self.client.post(url, data={"geom": "POINT(0 0)",
                                               "properties": '{"email_author": "x@x.x",  "date_observation": "2022-08-16", '
                                                             '"category": "Contribution Dégâts Potentiels",'
                                                             '"type": "Éboulements"}'})
        self.assertEqual(response.status_code, 201)
        self.assertEqual(ContributionPotentialDamage.objects.count(), 1)
        contribution = Contribution.objects.first()
        potential_damage = contribution.potential_damage
        self.assertEqual(contribution.email_author, 'x@x.x')
        self.assertEqual(potential_damage.get_type_display(), 'Éboulements')

    def test_contribution_category_does_not_exist(self):
        url = reverse('api_portal:contributions-list',
                      kwargs={'portal_pk': self.portal.pk, 'lang': 'fr'})
        response = self.client.post(url, data={"geom": "POINT(0 0)",
                                               "properties": '{"email_author": "x@x.x",  "date_observation": "2022-08-16", '
                                                             '"category": "Foo"}'})
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {'properties':
                                               ["'Foo' is not one of "
                                                "['Contribution Quantité', "
                                                "'Contribution Qualité', "
                                                "'Contribution Faune-Flore', "
                                                "'Contribution Élément Paysagers', "
                                                "'Contribution Dégâts Potentiels']"]})

    @mock.patch('georiviere.contribution.schema.get_contribution_properties')
    def test_contribution_category_model_does_not_exist(self, mocked):
        def json_property():
            json_schema_properties = {'name_author': {
                'type': "string",
                'title': "Name author",
                "maxLength": 128
            }, 'first_name_author': {
                'type': "string",
                'title': "First name author",
                "maxLength": 128
            }, 'email_author': {
                'type': "string",
                'title': "Email",
                'format': "email"
            }, 'date_observation': {
                'type': "string",
                'title': "Observation's date",
                'format': 'date'
            }, 'description': {
                'type': "string",
                'title': 'Description'
            }, 'category': {
                "type": "string",
                "title": "Category",
                "enum": [
                    'foo',
                ],
            }
            }
            return json_schema_properties
        mocked.side_effect = json_property
        url = reverse('api_portal:contributions-list',
                      kwargs={'portal_pk': self.portal.pk, 'lang': 'fr'})
        response = self.client.post(url, data={"geom": "POINT(0 0)",
                                               "properties": '{"email_author": "x@x.x",  "date_observation": "2022-08-16", '
                                                             '"category": "foo"}'})
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {'category': "La catégorie n'est pas valide"})
