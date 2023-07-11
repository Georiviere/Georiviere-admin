from django.test import TestCase

from georiviere.flatpages.tests.factories import FlatPageFactory


class FlatPageModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.flatpage = FlatPageFactory(title='foo bar')

    def test_str(self):
        self.assertEqual(str(self.flatpage), 'foo bar')

    def test_slug(self):
        self.assertEqual(self.flatpage.slug, 'foo-bar')
