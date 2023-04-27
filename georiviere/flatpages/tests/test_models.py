from django.core.exceptions import ValidationError
from django.test import TestCase

from georiviere.flatpages.forms import FlatPageForm
from georiviere.flatpages.tests.factories import FlatPageFactory
from mapentity.tests.factories import SuperUserFactory


class FlatPageModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.flatpage = FlatPageFactory(title='foo bar')

    def test_str(self):
        self.assertEqual(str(self.flatpage), 'foo bar')

    def test_slug(self):
        self.assertEqual(self.flatpage.slug, 'foo-bar')
