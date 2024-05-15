from django.core import mail
from django.test import override_settings, TestCase

from .factories import (
    ContributionFactory,
    ContributionPotentialDamageFactory,
    ContributionQualityFactory,
    ContributionQuantityFactory,
    ContributionFaunaFloraFactory,
    ContributionLandscapeElementsFactory,
    SeverityTypeTypeFactory,
    LandingTypeFactory,
    JamTypeFactory,
    DiseaseTypeFactory,
    DeadSpeciesFactory,
    InvasiveSpeciesFactory,
    HeritageSpeciesFactory,
    HeritageObservationFactory,
    FishSpeciesFactory,
    NaturePollutionFactory,
    TypePollutionFactory,
    ContributionStatusFactory,
    CustomContributionTypeFactory,
    CustomContributionTypeFieldFactory,
)
from ..models import CustomContributionTypeField


@override_settings(
    MANAGERS=[
        ("Fake", "fake@fake.fake"),
    ]
)
class ContributionMetaTest(TestCase):
    """Test for Contribution model"""

    @override_settings(MANAGERS=["fake@fake.fake"])
    def test_contribution_try_send_report_fail(self):
        self.assertEqual(len(mail.outbox), 0)
        contribution = ContributionFactory(email_author="mail.mail@mail")
        self.assertEqual(str(contribution), "mail.mail@mail")
        self.assertEqual(len(mail.outbox), 0)

    def test_contribution_str(self):
        ContributionStatusFactory(label="Informé")
        self.assertEqual(len(mail.outbox), 0)
        contribution = ContributionFactory(email_author="mail.mail@mail")
        self.assertEqual(str(contribution), "mail.mail@mail")
        self.assertEqual(contribution.category, "No category")
        self.assertEqual(len(mail.outbox), 1)

    def test_potentialdamage_str(self):
        self.assertEqual(len(mail.outbox), 0)
        potential_damage = ContributionPotentialDamageFactory(type=2)
        self.assertEqual(
            str(potential_damage),
            "Contribution Potential Damage Excessive cutting of riparian forest",
        )
        contribution = potential_damage.contribution
        self.assertEqual(
            str(contribution),
            f"{contribution.email_author} "
            f"Contribution Potential Damage Excessive cutting of riparian forest",
        )
        self.assertEqual(contribution.category, potential_damage)
        self.assertEqual(len(mail.outbox), 1)

    def test_quality_str(self):
        self.assertEqual(len(mail.outbox), 0)
        quality = ContributionQualityFactory(type=2)
        self.assertEqual(str(quality), "Contribution Quality Pollution")
        contribution = quality.contribution
        self.assertEqual(
            str(contribution),
            f"{contribution.email_author} " f"Contribution Quality Pollution",
        )
        self.assertEqual(contribution.category, quality)
        self.assertEqual(len(mail.outbox), 1)

    def test_quantity_str(self):
        self.assertEqual(len(mail.outbox), 0)
        quantity = ContributionQuantityFactory(type=2)
        self.assertEqual(
            str(quantity), "Contribution Quantity In the process of drying out"
        )
        contribution = quantity.contribution
        self.assertEqual(
            str(contribution),
            f"{contribution.email_author} "
            f"Contribution Quantity In the process of drying out",
        )
        self.assertEqual(contribution.category, quantity)
        self.assertEqual(len(mail.outbox), 1)

    def test_fauna_flora_str(self):
        self.assertEqual(len(mail.outbox), 0)
        fauna_flora = ContributionFaunaFloraFactory(type=2)
        self.assertEqual(str(fauna_flora), "Contribution Fauna-Flora Heritage species")
        contribution = fauna_flora.contribution
        self.assertEqual(
            str(contribution),
            f"{contribution.email_author} "
            f"Contribution Fauna-Flora Heritage species",
        )
        self.assertEqual(contribution.category, fauna_flora)
        self.assertEqual(len(mail.outbox), 1)

    def test_landscape_elements_str(self):
        self.assertEqual(len(mail.outbox), 0)
        landscape_elements = ContributionLandscapeElementsFactory(type=2)
        self.assertEqual(
            str(landscape_elements), "Contribution Landscape Element Fountain"
        )
        contribution = landscape_elements.contribution
        self.assertEqual(
            str(contribution),
            f"{contribution.email_author} " f"Contribution Landscape Element Fountain",
        )
        self.assertEqual(contribution.category, landscape_elements)
        self.assertEqual(len(mail.outbox), 1)

    def test_severitytype_str(self):
        severity_type = SeverityTypeTypeFactory(label="Severity type 1")
        self.assertEqual(str(severity_type), "Severity type 1")

    def test_contribution_category_display(self):
        contribution = ContributionFactory(email_author="mail.mail@mail")
        self.assertEqual(
            str(contribution.category_display),
            f'<a data-pk="{contribution.pk}" href="/contribution/{contribution.pk}/" title="No category" >No category</a>',
        )
        contribution.published = True
        contribution.save()
        self.assertEqual(
            contribution.category_display,
            f'<span class="badge badge-success" title="Published">&#x2606;</span> <a data-pk="{contribution.pk}" href="/contribution/{contribution.pk}/" title="No category" >No category</a>',
        )


class ContributionPotentialDamageTest(TestCase):
    """Test for Category potential damage model"""

    def test_landingtype_str(self):
        landing_type = LandingTypeFactory(label="Landing type 1")
        self.assertEqual(str(landing_type), "Landing type 1")

    def test_jamtype_str(self):
        jam_type = JamTypeFactory(label="Jam type 1")
        self.assertEqual(str(jam_type), "Jam type 1")

    def test_diseasetype_str(self):
        disease_type = DiseaseTypeFactory(label="Disease type 1")
        self.assertEqual(str(disease_type), "Disease type 1")

    def test_deadspecies_str(self):
        dead_species = DeadSpeciesFactory(label="Dead species 1")
        self.assertEqual(str(dead_species), "Dead species 1")


class ContributionFaunaFloraTest(TestCase):
    """Test for Category potential damage model"""

    def test_invasivespecies_str(self):
        invasive_species = InvasiveSpeciesFactory(label="Invasive species 1")
        self.assertEqual(str(invasive_species), "Invasive species 1")

    def test_heritagespecies_str(self):
        heritage_species = HeritageSpeciesFactory(label="Heritage species 1")
        self.assertEqual(str(heritage_species), "Heritage species 1")

    def test_heritageobservations_str(self):
        heritage_observation = HeritageObservationFactory(
            label="Heritage observation 1"
        )
        self.assertEqual(str(heritage_observation), "Heritage observation 1")

    def test_fishspecies_str(self):
        fish_species = FishSpeciesFactory(label="Fish species 1")
        self.assertEqual(str(fish_species), "Fish species 1")


class ContributionNaturePollutionTest(TestCase):
    """Test for Category potential damage model"""

    def test_naturepollution_str(self):
        nature_pollution = NaturePollutionFactory(label="Nature pollution 1")
        self.assertEqual(str(nature_pollution), "Nature pollution 1")

    def test_typepollution_str(self):
        type_pollution = TypePollutionFactory(label="Type pollution 1")
        self.assertEqual(str(type_pollution), "Type pollution 1")


class ContributionStatusTest(TestCase):
    """Test for Status Contribution model"""

    def test_status_str(self):
        nature_pollution = ContributionStatusFactory(label="Contribution status 1")
        self.assertEqual(str(nature_pollution), "Contribution status 1")


class CustomContributionTypeTestCase(TestCase):
    def test_str(self):
        """CustomContributionType should return its label as string representation"""
        custom_contribution_type = CustomContributionTypeFactory.create()
        self.assertEqual(str(custom_contribution_type), custom_contribution_type.label)

    def test_json_schema_empty(self):
        custom_contribution_type = CustomContributionTypeFactory.create()
        self.assertDictEqual(
            custom_contribution_type.json_schema_form,
            {"type": "object", "properties": {}, "required": []},
        )

    def test_json_schema_required_field(self):
        """CustomContributionType JSON schema should include required fields in dedicated key"""
        custom_contribution_type = CustomContributionTypeFactory.create()
        required_field = CustomContributionTypeFieldFactory.create(
            custom_type=custom_contribution_type, required=True
        )
        optional_field = CustomContributionTypeFieldFactory.create(
            custom_type=custom_contribution_type, required=False
        )
        json_schema = custom_contribution_type.json_schema_form
        self.assertIn(required_field.key, json_schema["required"])
        self.assertNotIn(optional_field.key, json_schema["required"])


class CustomContributionTypeFieldTestCase(TestCase):
    def test_str(self):
        """CustomContributionTypeField should return its label / value as string representation"""
        field = CustomContributionTypeFieldFactory.create()
        self.assertEqual(str(field), f"{field.label}: ({field.value_type})")

    def test_specific_slug(self):
        """CustomContributionTypeField generated key is its slugged label, but '-' should be replaced by '_'"""
        field = CustomContributionTypeFieldFactory.create(label="Field label")
        self.assertEqual(field.key, "field_label")

    def test_type_string_schema_without_customization(self):
        field = CustomContributionTypeFieldFactory.create(
            value_type=CustomContributionTypeField.FieldTypeChoices.STRING
        )
        self.assertDictEqual(
            field.get_field_schema(),
            {"type": "string", "helpText": "", "title": field.label},
        )

    def test_type_string_schema_with_customization(self):
        field = CustomContributionTypeFieldFactory.create(
            value_type=CustomContributionTypeField.FieldTypeChoices.STRING,
            help_text="Field help text",
            customization={
                "choices": ["choice1", "choice2"],
                "placeholder": "placeholder",
                "minLength": 1,
                "maxLength": 10,
            },
        )
        self.assertDictEqual(
            field.get_field_schema(),
            {
                "helpText": field.help_text,
                "title": field.label,
                "type": "string",
                **field.customization,
            },
        )

    def test_type_text_schema_without_customization(self):
        field = CustomContributionTypeFieldFactory.create(
            value_type=CustomContributionTypeField.FieldTypeChoices.TEXT
        )
        self.assertDictEqual(
            field.get_field_schema(),
            {
                "type": "string",
                "helpText": "",
                "title": field.label,
                "widget": "textarea",
            },
        )

    def test_type_text_schema_with_customization(self):
        field = CustomContributionTypeFieldFactory.create(
            value_type=CustomContributionTypeField.FieldTypeChoices.TEXT,
            help_text="Field help text",
            customization={
                "widget": "textarea",
                "placeholder": "placeholder",
                "minLength": 1,
                "maxLength": 10,
            },
        )
        self.assertDictEqual(
            field.get_field_schema(),
            {
                "helpText": field.help_text,
                "title": field.label,
                "type": "string",
                "widget": "textarea",
                **field.customization,
            },
        )

    def test_type_integer_schema_without_customization(self):
        field = CustomContributionTypeFieldFactory.create(
            value_type=CustomContributionTypeField.FieldTypeChoices.INTEGER
        )
        self.assertDictEqual(
            field.get_field_schema(),
            {"type": "integer", "helpText": "", "title": field.label},
        )

    def test_type_integer_schema_with_customization(self):
        field = CustomContributionTypeFieldFactory.create(
            value_type=CustomContributionTypeField.FieldTypeChoices.INTEGER,
            help_text="Field help text",
            customization={"minimum": 0, "maximum": 10},
        )
        self.assertDictEqual(
            field.get_field_schema(),
            {
                "helpText": field.help_text,
                "title": field.label,
                "type": "integer",
                **field.customization,
            },
        )

    def test_type_float_schema_without_customization(self):
        field = CustomContributionTypeFieldFactory.create(
            value_type=CustomContributionTypeField.FieldTypeChoices.FLOAT
        )
        self.assertDictEqual(
            field.get_field_schema(),
            {"type": "number", "helpText": "", "title": field.label},
        )

    def test_type_float_schema_with_customization(self):
        field = CustomContributionTypeFieldFactory.create(
            value_type=CustomContributionTypeField.FieldTypeChoices.FLOAT,
            help_text="Field help text",
            customization={"minimum": 0, "maximum": 10},
        )
        self.assertDictEqual(
            field.get_field_schema(),
            {
                "helpText": field.help_text,
                "title": field.label,
                "type": "number",
                **field.customization,
            },
        )

    def test_type_boolean_schema_without_customization(self):
        field = CustomContributionTypeFieldFactory.create(
            value_type=CustomContributionTypeField.FieldTypeChoices.BOOLEAN
        )
        self.assertDictEqual(
            field.get_field_schema(),
            {"type": "boolean", "helpText": "", "title": field.label},
        )

    def test_type_boolean_schema_with_customization(self):
        field = CustomContributionTypeFieldFactory.create(
            value_type=CustomContributionTypeField.FieldTypeChoices.BOOLEAN,
            help_text="Field help text",
            customization={
                "widget": "radio",
                "choices": [
                    {"title": "Yes", "value": True},
                    {"title": "No", "value": False},
                ],
            },
        )
        self.assertDictEqual(
            field.get_field_schema(),
            {
                "helpText": field.help_text,
                "title": field.label,
                "type": "boolean",
                **field.customization,
            },
        )

    def test_type_date_schema_without_customization(self):
        field = CustomContributionTypeFieldFactory.create(
            value_type=CustomContributionTypeField.FieldTypeChoices.DATE
        )
        self.assertDictEqual(
            field.get_field_schema(),
            {"type": "string", "format": "date", "helpText": "", "title": field.label},
        )

    def test_type_datetime_schema_without_customization(self):
        field = CustomContributionTypeFieldFactory.create(
            value_type=CustomContributionTypeField.FieldTypeChoices.DATETIME
        )
        self.assertDictEqual(
            field.get_field_schema(),
            {"type": "string", "format": "date-time", "helpText": "", "title": field.label},
        )

    def test_dropped_choices_empty(self):
        """ If choices is defined but empty, it should not be included in the schema """
        field = CustomContributionTypeFieldFactory.create(
            value_type=CustomContributionTypeField.FieldTypeChoices.STRING,
            customization={
                "choices": [],
            },
        )
        self.assertNotIn(
            'choices',
            field.get_field_schema(),
        )
