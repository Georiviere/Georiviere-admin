from django.test import TestCase
from django.urls import reverse

from mapentity.tests.factories import SuperUserFactory

from georiviere.contribution.tests.factories import CustomContributionTypeFactory, CustomContributionTypeFieldFactory, \
    CustomContributionFactory
from georiviere.main.tests.factories import AttachmentFactory


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


class CustomContributionAdminTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.super_user = SuperUserFactory.create()
        cls.custom_contribution_type = CustomContributionTypeFactory.create()

    def setUp(self):
        self.client.force_login(self.super_user)

    def test_list_customcontributiontype_admin_view(self):
        url_list = reverse('admin:contribution_customcontributiontype_changelist')
        response = self.client.get(url_list)
        self.assertEqual(response.status_code, 200)

    def test_detail_customcontributiontype_admin_view(self):
        url_detail = reverse('admin:contribution_customcontributiontype_change',
                             args=[self.custom_contribution_type.pk])
        response = self.client.get(url_detail)
        self.assertEqual(response.status_code, 200)

    def test_get_customcontributiontype_add_admin_view(self):
        url_add = reverse('admin:contribution_customcontributiontype_add')
        response = self.client.get(url_add)
        self.assertEqual(response.status_code, 200)


class CustomContributionTypeFieldAdminTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.super_user = SuperUserFactory.create()
        cls.custom_contribution_type = CustomContributionTypeFactory.create()
        cls.field = CustomContributionTypeFieldFactory.create(custom_type=cls.custom_contribution_type)

    def setUp(self):
        self.client.force_login(self.super_user)

    def test_list_customcontributiontypefield_admin_view(self):
        url_list = reverse('admin:contribution_customcontributiontypefield_changelist')
        response = self.client.get(url_list)
        self.assertEqual(response.status_code, 200)

    def test_detail_customcontributiontypefield_admin_view(self):
        """ Detail view of a custom type field in admin (extra config) """
        url_detail = reverse('admin:contribution_customcontributiontypefield_change',
                             args=[self.field.pk])
        response = self.client.get(url_detail)
        self.assertEqual(response.status_code, 200)

    def test_get_customcontributiontypefield_add_admin_view(self):
        """ Unable to add custom type field directly by admin """
        url_add = reverse('admin:contribution_customcontributiontypefield_add')
        response = self.client.get(url_add)
        self.assertEqual(response.status_code, 403)


class CustomContributionAdminTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.super_user = SuperUserFactory.create()
        cls.simple_contrib = CustomContributionFactory(geom='SRID=2154;POINT(700000 6600000)')
        cls.contrib_with_attachments = CustomContributionFactory(geom='SRID=2154;POINT(700000 6600000)')
        AttachmentFactory.create_batch(2, content_object=cls.contrib_with_attachments)

    def setUp(self):
        self.client.force_login(self.super_user)

    def test_list_custom_contribution_admin_view(self):
        url_list = reverse('admin:contribution_customcontribution_changelist')
        response = self.client.get(url_list)
        self.assertEqual(response.status_code, 200)

    def test_detail_custom_contribution_admin_view(self):
        url_detail = reverse('admin:contribution_customcontribution_change',
                             args=[self.contrib_with_attachments.pk])
        response = self.client.get(url_detail)
        self.assertEqual(response.status_code, 200)
