from django.test import TestCase
from django.urls import reverse

from mapentity.tests.factories import SuperUserFactory


class ContributionAdminTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.super_user = SuperUserFactory.create()

    def setUp(self):
        self.client.force_login(self.super_user)

    def test_get_severitytype_add_admin_view(self):
        url_add = reverse('admin:contribution_severitytype_add')
        response = self.client.get(url_add)
        self.assertEqual(response.status_code, 200)

    def test_get_landingtype_add_admin_view(self):
        url_add = reverse('admin:contribution_landingtype_add')
        response = self.client.get(url_add)
        self.assertEqual(response.status_code, 200)

    def test_get_jamtype_add_admin_view(self):
        url_add = reverse('admin:contribution_jamtype_add')
        response = self.client.get(url_add)
        self.assertEqual(response.status_code, 200)

    def test_get_diseasetype_add_admin_view(self):
        url_add = reverse('admin:contribution_diseasetype_add')
        response = self.client.get(url_add)
        self.assertEqual(response.status_code, 200)

    def test_get_deadspecies_add_admin_view(self):
        url_add = reverse('admin:contribution_deadspecies_add')
        response = self.client.get(url_add)
        self.assertEqual(response.status_code, 200)

    def test_get_invasivespecies_add_admin_view(self):
        url_add = reverse('admin:contribution_invasivespecies_add')
        response = self.client.get(url_add)
        self.assertEqual(response.status_code, 200)

    def test_get_heritagespecies_add_admin_view(self):
        url_add = reverse('admin:contribution_heritagespecies_add')
        response = self.client.get(url_add)
        self.assertEqual(response.status_code, 200)

    def test_get_heritageobservation_add_admin_view(self):
        url_add = reverse('admin:contribution_heritageobservation_add')
        response = self.client.get(url_add)
        self.assertEqual(response.status_code, 200)

    def test_get_fishspecies_add_admin_view(self):
        url_add = reverse('admin:contribution_fishspecies_add')
        response = self.client.get(url_add)
        self.assertEqual(response.status_code, 200)

    def test_get_naturepollution_add_admin_view(self):
        url_add = reverse('admin:contribution_naturepollution_add')
        response = self.client.get(url_add)
        self.assertEqual(response.status_code, 200)

    def test_get_typepollution_add_admin_view(self):
        url_add = reverse('admin:contribution_typepollution_add')
        response = self.client.get(url_add)
        self.assertEqual(response.status_code, 200)
