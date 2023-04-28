from django.core.exceptions import ValidationError
from django.test import TestCase

from georiviere.flatpages.forms import FlatPageForm
from georiviere.flatpages.tests.factories import FlatPageFactory
from mapentity.tests.factories import SuperUserFactory


class FlatPageAdminTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = SuperUserFactory.create()
        cls.flatpage = FlatPageFactory()

    def setUp(self):
        self.client.force_login(self.user)

    def test_flatpages_are_registered(self):
        response = self.client.get('/admin/flatpages/flatpage/')
        self.assertEqual(response.status_code, 200)

    def test_flatpages_contain_tiny_mce(self):
        response = self.client.get('/admin/flatpages/flatpage/add/')
        self.assertContains(response, 'tiny-class')


class FlatPageFormTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = SuperUserFactory.create()
        cls.flatpage = FlatPageFactory()

    def test_flatpages_content_external_url_fill(self):
        data = {
            'title': self.flatpage.title,
            'content': 'content',
            'external_url': 'http://foo.foo',
            'portals': self.flatpage.portals,
            'order': self.flatpage.order,
            'hidden': False
        }

        form = FlatPageForm(user=self.user, instance=self.flatpage, data=data)

        self.assertFalse(form.is_valid())
        with self.assertRaisesRegex(ValidationError, "Choose between external URL and HTML content"):
            form.clean()

    def test_flatpages_content_fill(self):
        data = {
            'title': self.flatpage.title,
            'content': 'content',
            'external_url': '',
            'portals': [portal for portal in self.flatpage.portals.all()],
            'order': self.flatpage.order,
            'hidden': False
        }

        form = FlatPageForm(user=self.user, instance=self.flatpage, data=data)

        self.assertTrue(form.is_valid())

    def test_flatpages_external_url_fill(self):
        data = {
            'title': self.flatpage.title,
            'content': '',
            'external_url': 'http://foo.foo',
            'portals': [portal for portal in self.flatpage.portals.all()],
            'order': self.flatpage.order,
            'hidden': False
        }

        form = FlatPageForm(user=self.user, instance=self.flatpage, data=data)

        self.assertTrue(form.is_valid())
