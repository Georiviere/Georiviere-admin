from django.test import TestCase
from geotrek.common.utils.testdata import get_dummy_uploaded_image

from mapentity.tests.factories import SuperUserFactory, UserFactory
from unittest import mock

from .factories import AttachmentFactory

from georiviere.river.tests.factories import StreamFactory
from georiviere.portal.tests.factories import PortalFactory
from georiviere.valorization.tests.factories import POIFactory


class AttachmentTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = UserFactory(username='foo')
        cls.superuser = SuperUserFactory(username='bar')
        cls.poi = POIFactory.create()
        cls.image = get_dummy_uploaded_image()
        cls.attachment_image_poi = AttachmentFactory.create(content_object=cls.poi,
                                                            attachment_file=cls.image)
        cls.portal = PortalFactory.create()
        cls.stream = StreamFactory.create()
        cls.image = get_dummy_uploaded_image()
        cls.attachment_image_stream = AttachmentFactory.create(content_object=cls.stream,
                                                               attachment_file=cls.image)

    def test_get_attachment_without_authenticated(self):
        response = self.client.get(self.attachment_image_poi.attachment_file.url)
        self.assertEqual(response.status_code, 403)

    def test_get_attachment_without_permission_read_attachment(self):
        self.client.force_login(user=self.user)
        response = self.client.get(self.attachment_image_poi.attachment_file.url)
        self.assertEqual(response.status_code, 403)

    @mock.patch('django.contrib.auth.models.PermissionsMixin.has_perm')
    def test_get_attachment_without_permission_read_object(self, mocke):
        def user_perms(p, obj=None):
            return {'common.read_attachment': True}.get(p, False)
        mocke.side_effect = user_perms
        self.client.force_login(user=self.user)
        response = self.client.get(self.attachment_image_poi.attachment_file.url)
        self.assertEqual(response.status_code, 403)

    def test_get_attachment_poi(self):
        self.client.force_login(user=self.superuser)
        response = self.client.get(self.attachment_image_poi.attachment_file.url)
        self.assertEqual(response.status_code, 200)

    @mock.patch('django.contrib.auth.models.PermissionsMixin.has_perm')
    def test_get_attachment_without_permission_read_poi_is_public(self, mocke):
        def user_perms(p, obj=None):
            return {'common.read_attachment': True}.get(p, False)
        mocke.side_effect = user_perms
        self.client.force_login(user=self.user)
        self.poi.portals.add(self.portal)
        response = self.client.get(self.attachment_image_poi.attachment_file.url)
        self.assertEqual(response.status_code, 200)

    def test_get_attachment_stream(self):
        self.client.force_login(user=self.superuser)
        response = self.client.get(self.attachment_image_stream.attachment_file.url)
        self.assertEqual(response.status_code, 200)

    @mock.patch('django.contrib.auth.models.PermissionsMixin.has_perm')
    def test_get_attachment_without_permission_read_stream_is_public(self, mocke):
        def user_perms(p, obj=None):
            return {'common.read_attachment': True}.get(p, False)
        mocke.side_effect = user_perms
        self.client.force_login(user=self.user)
        self.stream.portals.add(self.portal)
        response = self.client.get(self.attachment_image_stream.attachment_file.url)
        self.assertEqual(response.status_code, 200)
