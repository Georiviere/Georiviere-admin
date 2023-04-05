from django.test import TestCase

from georiviere.tests.factories import UserAllPermsFactory
from . import factories
from ..forms import StationForm


class StationFormTestCase(TestCase):
    """Test form station"""

    @classmethod
    def setUpTestData(cls):

        cls.user = UserAllPermsFactory()
        cls.station1 = factories.StationFactory(
            label="Station 1",
            code="1234"
        )

    def test_duplicate_code_error(self):
        """Test error on form if station with duplicated code key is created"""
        success = self.client.force_login(self.user)
        self.assertTrue(success)
        station2_form = StationForm(user=self.user, data={"label": "Station 2", "code": "1234"})
        station2_form.is_valid()
        self.assertIn('code', station2_form.errors)
        station1_edit_form = StationForm(user=self.user, instance=self.station1, data={"label": "Station 1 etc", "code": "1234"})
        station1_edit_form.is_valid()
        self.assertNotIn('code', station1_edit_form.errors)
