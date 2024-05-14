from django.test import TestCase
from django_jsonform.forms.fields import JSONFormField

from georiviere.tests.factories import UserAllPermsFactory

from ...observations.tests.factories import StationFactory
from ..forms import ContributionForm, CustomContributionForm
from ..models import CustomContribution, CustomContributionType
from . import factories
from .factories import CustomContributionFactory, CustomContributionTypeFactory


class ContributionFormTestCase(TestCase):
    """Test form contribution"""

    @classmethod
    def setUpTestData(cls):

        cls.user = UserAllPermsFactory()
        cls.quantity = factories.ContributionQuantityFactory()

    def test_contribution(self):
        self.client.force_login(self.user)
        contribution_form = ContributionForm(
            user=self.user,
            instance=self.quantity.contribution,
            data={
                "geom": self.quantity.contribution.geom,
                "email_author": self.quantity.contribution.email_author,
            },
            can_delete=False,
        )
        self.assertEqual(True, contribution_form.is_valid())


class CustomContributionFormTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.custom_type = CustomContributionTypeFactory()
        cls.custom_type_with_station = CustomContributionTypeFactory()
        cls.custom_type_with_station.stations.add(StationFactory())
        cls.contribution = CustomContributionFactory(custom_type=cls.custom_type)
        cls.contribution_with_station = CustomContributionFactory(
            custom_type=cls.custom_type_with_station
        )

    def test_station_field_disabled_by_default(self):
        form = CustomContributionForm(instance=self.contribution)
        self.assertTrue(form.fields["station"].disabled)

    def test_station_field_enabled_when_station_exists(self):
        form = CustomContributionForm(instance=self.contribution_with_station)
        self.assertFalse(form.fields["station"].disabled)

    def test_station_field_required_when_station_exists(self):
        form = CustomContributionForm(instance=self.contribution_with_station)
        self.assertTrue(form.fields["station"].required)

    def test_data_field_is_jsonformfield_when_instance_exists(self):
        form = CustomContributionForm(instance=self.contribution)
        self.assertIsInstance(form.fields["data"], JSONFormField)

    def test_data_field_schema_is_correct_when_instance_exists(self):
        form = CustomContributionForm(instance=self.contribution)
        self.assertEqual(
            form.fields["data"].widget.schema,
            self.contribution.custom_type.get_json_schema_form(),
        )
