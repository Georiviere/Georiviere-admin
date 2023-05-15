from django.test import TestCase

from georiviere.portal.tests.factories import PortalFactory
from georiviere.api.valorization.serializers.portal import PortalSerializer


class PortalSerializerTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.portal = PortalFactory.create()
        cls.serializer_portal = PortalSerializer(instance=cls.portal)

    def test_portal_content(self):
        data = self.serializer_portal.data
        self.assertSetEqual(set(data.keys()), {'id', 'map', 'name', 'group'})
