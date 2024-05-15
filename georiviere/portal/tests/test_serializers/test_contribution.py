import os

from django.test import TestCase
import json

from georiviere.contribution.models import CustomContribution
from georiviere.observations.tests.factories import StationFactory
from georiviere.portal.validators import validate_json_schema

from georiviere.contribution.tests.factories import (TypePollutionFactory, NaturePollutionFactory,
                                                     FishSpeciesFactory, InvasiveSpeciesFactory, DeadSpeciesFactory,
                                                     HeritageObservationFactory, HeritageSpeciesFactory,
                                                     DiseaseTypeFactory, LandingTypeFactory, SeverityTypeTypeFactory,
                                                     JamTypeFactory, CustomContributionTypeFactory,
                                                     CustomContributionTypeBooleanFieldFactory,
                                                     CustomContributionTypeFloatFieldFactory,
                                                     CustomContributionTypeIntegerFieldFactory,
                                                     CustomContributionTypeStringFieldFactory,
                                                     CustomContributionTypeTextFieldFactory,
                                                     CustomContributionTypeDateFieldFactory,
                                                     CustomContributionTypeDatetimeFieldFactory,
                                                     CustomContributionFactory)

from georiviere.portal.serializers.contribution import ContributionSchemaSerializer, CustomContributionSerializer


# TODO: Add tests on every possibilities validate with json schema


class ContributionSchemaSerializerTest(TestCase):
    def test_contribution_without_subtypes(self):
        serializer_contribution = ContributionSchemaSerializer({})
        data = serializer_contribution.data
        validate_json_schema(data)
        filename = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data',
                                'json_schema_base_contribution_without_subtypes.json')
        with open(filename) as f:
            json_data = json.load(f)
        self.assertEqual(json_data, data)

    def test_contribution_with_subtypes(self):
        JamTypeFactory.reset_sequence()
        JamTypeFactory.create_batch(3)
        SeverityTypeTypeFactory.reset_sequence()
        SeverityTypeTypeFactory.create_batch(3)
        TypePollutionFactory.reset_sequence()
        TypePollutionFactory.create_batch(3)
        NaturePollutionFactory.reset_sequence()
        NaturePollutionFactory.create_batch(3)
        FishSpeciesFactory.reset_sequence()
        FishSpeciesFactory.create_batch(3)
        InvasiveSpeciesFactory.reset_sequence()
        InvasiveSpeciesFactory.create_batch(3)
        DeadSpeciesFactory.reset_sequence()
        DeadSpeciesFactory.create_batch(3)
        HeritageObservationFactory.reset_sequence()
        HeritageObservationFactory.create_batch(3)
        HeritageSpeciesFactory.reset_sequence()
        HeritageSpeciesFactory.create_batch(3)
        DiseaseTypeFactory.reset_sequence()
        DiseaseTypeFactory.create_batch(3)
        LandingTypeFactory.reset_sequence()
        LandingTypeFactory.create_batch(3)
        serializer_contribution = ContributionSchemaSerializer({})
        data = serializer_contribution.data
        validate_json_schema(data)
        filename = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data',
                                'json_schema_base_contribution.json')
        with open(filename) as f:
            json_data = json.load(f)
        self.assertEqual(json_data, data)


class CustomContributionSerializerTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.custom_contrib_type = CustomContributionTypeFactory()
        cls.bool_field = CustomContributionTypeBooleanFieldFactory(custom_type=cls.custom_contrib_type)
        cls.float_field = CustomContributionTypeFloatFieldFactory(custom_type=cls.custom_contrib_type)
        cls.integer_field = CustomContributionTypeIntegerFieldFactory(custom_type=cls.custom_contrib_type)
        cls.string_field = CustomContributionTypeStringFieldFactory(custom_type=cls.custom_contrib_type)
        cls.text_field = CustomContributionTypeTextFieldFactory(custom_type=cls.custom_contrib_type)
        cls.date_field = CustomContributionTypeDateFieldFactory(custom_type=cls.custom_contrib_type)
        cls.datetime_field = CustomContributionTypeDatetimeFieldFactory(custom_type=cls.custom_contrib_type)
        cls.custom_contrib = CustomContributionFactory(
            custom_type=cls.custom_contrib_type,
            data={
                cls.bool_field.key: True,
                cls.float_field.key: 1.0,
                cls.integer_field.key: 1,
                cls.string_field.key: "toto",
                cls.text_field.key: "toto",
                cls.date_field.key: "2020-01-01",
                cls.datetime_field.key: "2020-01-01T00:00:00Z"
            }
        )

    def get_serializer_context(self):
        return {
            "lang": "fr",
            "portal_pk": 1,
            "custom_type": self.custom_contrib_type
        }

    def get_serializer(self, **kwargs):
        custom_contrib = (CustomContribution.objects.with_type_values(self.custom_contrib_type)
                          .get(pk=self.custom_contrib.pk))
        return CustomContributionSerializer(custom_contrib, context=self.get_serializer_context(), **kwargs)

    def get_serializer_data(self):
        serializer = self.get_serializer()
        return serializer.data

    def test_full_render(self):
        data = self.get_serializer_data()
        fields = list(data.keys())
        self.assertIn(self.bool_field.key, fields)
        self.assertIn(self.integer_field.key, fields)
        self.assertIn(self.float_field.key, fields)
        self.assertIn(self.string_field.key, fields)
        self.assertIn(self.text_field.key, fields)
        self.assertIn(self.date_field.key, fields)
        self.assertIn(self.datetime_field.key, fields)

    def test_station_required_if_linked_to_custom_type(self):
        self.custom_contrib_type.stations.add(StationFactory())
        serializer = self.get_serializer()
        self.assertTrue(serializer.fields['station'].required)

    def test_station_not_required_if_linked_to_custom_type(self):
        serializer = self.get_serializer()
        self.assertFalse(serializer.fields['station'].required)

    def test_password_field_not_exists_if_not_defined_in_custom_type(self):
        serializer = self.get_serializer()
        self.assertNotIn('password', serializer.fields)

    def test_password_is_required_if_defined_in_custom_type(self):
        self.custom_contrib_type.password = "toto"
        self.custom_contrib_type.save()
        serializer = self.get_serializer()
        self.assertTrue(serializer.fields['password'].required)

    def test_password_should_match_if_defined_in_custom_type(self):
        self.custom_contrib_type.password = "toto"
        self.custom_contrib_type.save()
        serializer = self.get_serializer(data={"password": "toto"})
        serializer.is_valid()
        self.assertNotIn('password', serializer.errors)
        serializer = self.get_serializer(data={"password": "tata"})
        serializer.is_valid()
        self.assertIn('password', serializer.errors)

    def test_with_no_custom_type_in_context(self):
        serializer = CustomContributionSerializer(self.custom_contrib, context={"lang": "fr", "portal_pk": 1})
        self.assertNotIn(self.bool_field.key, serializer.data)
