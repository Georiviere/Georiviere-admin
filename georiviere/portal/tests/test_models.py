from django.test import TestCase

from . import factories


class PortalTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.portal = factories.PortalFactory(
            name="Name portal",
        )

    def test_str(self):
        self.assertEqual(str(self.portal), "Name portal")
