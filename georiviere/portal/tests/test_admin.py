from django.test import TestCase
from django.urls import reverse

from . import factories

from mapentity.tests.factories import SuperUserFactory

from georiviere.portal.admin import MapLayerAdminForm, MapLayerAdminTabularForm


class PortalAdminTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.portal = factories.PortalFactory(
            name="Name portal",
        )
        cls.super_user = SuperUserFactory.create()

    def setUp(self):
        self.client.force_login(self.super_user)

    def test_get_add_admin_view(self):
        url_add = reverse('admin:portal_portal_add')
        response = self.client.get(url_add)
        self.assertEqual(response.status_code, 200)

    def test_form_maplayer_portal_tabular(self):
        form_data = {'label': 'New label', 'order': 1}
        self.portal.layers.first()
        form = MapLayerAdminTabularForm(instance=self.portal.layers.first(), data=form_data)
        self.assertTrue(form.is_valid())

    def test_form_maplayer(self):
        form_data = {'label': 'New label', 'order': 1}
        self.portal.layers.first()
        form = MapLayerAdminForm(instance=self.portal.layers.first(), data=form_data)
        self.assertTrue(form.is_valid())


class MapGroupLayerAdminTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.portal = factories.PortalFactory(
            name="Name portal",
        )
        cls.super_user = SuperUserFactory.create()
        cls.group_layer = factories.GroupMapLayerFactory()

    def setUp(self):
        self.client.force_login(self.super_user)

    def test_get_add_admin_view(self):
        url_add = reverse('admin:portal_mapgrouplayer_add')
        response = self.client.get(url_add)
        self.assertEqual(response.status_code, 200)

    def test_get_change_admin_view(self):
        url_add = reverse('admin:portal_mapgrouplayer_change', args=[self.group_layer.pk])
        response = self.client.get(url_add)
        self.assertEqual(response.status_code, 200)
