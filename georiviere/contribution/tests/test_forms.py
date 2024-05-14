from django.test import TestCase
from django_jsonform.forms.fields import JSONFormField

from georiviere.tests.factories import UserAllPermsFactory

from ...observations.tests.factories import StationFactory
from ..forms import (
    ContributionForm,
    CustomContributionFieldForm,
    CustomContributionFieldInlineForm,
    CustomContributionForm,
)
from . import factories
from .factories import (
    CustomContributionFactory,
    CustomContributionTypeBooleanFieldFactory,
    CustomContributionTypeDateFieldFactory,
    CustomContributionTypeDatetimeFieldFactory,
    CustomContributionTypeFactory,
    CustomContributionTypeFieldFactory,
    CustomContributionTypeFloatFieldFactory,
    CustomContributionTypeIntegerFieldFactory,
)


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


class CustomContributionFieldInlineFormTest(TestCase):
    def setUp(self):
        self.field = CustomContributionTypeFieldFactory()

    def test_value_type_field_disabled_when_instance_exists(self):
        form = CustomContributionFieldInlineForm(instance=self.field)
        self.assertTrue(form.fields["value_type"].disabled)

    def test_value_type_field_help_text_when_instance_exists(self):
        form = CustomContributionFieldInlineForm(instance=self.field)
        self.assertEqual(
            form.fields["value_type"].help_text,
            "You can't change value type after creation. Delete and/or create another one.",
        )


class CustomContributionFieldFormTest(TestCase):
    def test_schema_string(self):
        field = CustomContributionTypeFieldFactory(value_type="string")
        form = CustomContributionFieldForm(instance=field)
        self.assertIsInstance(form.fields["customization"], JSONFormField)

    def test_schema_integer(self):
        field = CustomContributionTypeIntegerFieldFactory()
        form = CustomContributionFieldForm(instance=field)
        self.assertIsInstance(form.fields["customization"], JSONFormField)

    def test_schema_number(self):
        field = CustomContributionTypeFloatFieldFactory()
        form = CustomContributionFieldForm(instance=field)
        self.assertIsInstance(form.fields["customization"], JSONFormField)

    def test_schema_boolean(self):
        field = CustomContributionTypeBooleanFieldFactory()
        form = CustomContributionFieldForm(instance=field)
        self.assertIsInstance(form.fields["customization"], JSONFormField)

    def test_schema_date(self):
        field = CustomContributionTypeDateFieldFactory()
        form = CustomContributionFieldForm(instance=field)
        self.assertIsInstance(form.fields["customization"], JSONFormField)

    def test_schema_datetime(self):
        field = CustomContributionTypeDatetimeFieldFactory()
        form = CustomContributionFieldForm(instance=field)
        self.assertIsInstance(form.fields["customization"], JSONFormField)
