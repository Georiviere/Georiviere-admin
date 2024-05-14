import datetime

from django.test import TestCase
from pytz import UTC

from georiviere.contribution.models import (
    CustomContribution,
    CustomContributionTypeField,
)
from georiviere.contribution.tests.factories import (
    CustomContributionFactory,
    CustomContributionTypeFactory,
    CustomContributionTypeFieldFactory,
)


class CustomContributionManagerTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.custom_contrib_type = CustomContributionTypeFactory()
        CustomContributionTypeFieldFactory(
            custom_type=cls.custom_contrib_type,
            value_type=CustomContributionTypeField.FieldTypeChoices.STRING,
            label="Field string",
        )
        CustomContributionTypeFieldFactory(
            custom_type=cls.custom_contrib_type,
            value_type=CustomContributionTypeField.FieldTypeChoices.BOOLEAN,
            label="Field boolean",
        )
        CustomContributionTypeFieldFactory(
            custom_type=cls.custom_contrib_type,
            value_type=CustomContributionTypeField.FieldTypeChoices.INTEGER,
            label="Field integer",
        )
        CustomContributionTypeFieldFactory(
            custom_type=cls.custom_contrib_type,
            value_type=CustomContributionTypeField.FieldTypeChoices.FLOAT,
            label="Field float",
        )
        CustomContributionTypeFieldFactory(
            custom_type=cls.custom_contrib_type,
            value_type=CustomContributionTypeField.FieldTypeChoices.TEXT,
            label="Field text",
        )
        CustomContributionTypeFieldFactory(
            custom_type=cls.custom_contrib_type,
            value_type=CustomContributionTypeField.FieldTypeChoices.DATE,
            label="Field date",
        )
        CustomContributionTypeFieldFactory(
            custom_type=cls.custom_contrib_type,
            value_type=CustomContributionTypeField.FieldTypeChoices.DATETIME,
            label="Field datetime",
        )
        CustomContributionFactory(
            custom_type=cls.custom_contrib_type,
            data={
                "field_string": "string",
                "field_boolean": True,
                "field_integer": 42,
                "field_float": 42.42,
                "field_text": "text",
                "field_date": "2020-01-01",
                "field_datetime": "2020-01-01T00:00:00Z",
            },
        )

    def test_annotated_queryset(self):
        qs = CustomContribution.objects.with_type_values(self.custom_contrib_type)
        instance = qs.first()
        self.assertEqual(instance.field_string, "string")
        self.assertEqual(instance.field_boolean, True)
        self.assertEqual(instance.field_integer, 42)
        self.assertEqual(instance.field_float, 42.42)
        self.assertEqual(instance.field_text, "text")
        self.assertEqual(instance.field_date, datetime.date(2020, 1, 1))
        self.assertEqual(
            instance.field_datetime, datetime.datetime(2020, 1, 1, 0, 0, tzinfo=UTC)
        )
