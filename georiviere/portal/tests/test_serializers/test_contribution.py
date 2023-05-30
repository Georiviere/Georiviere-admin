import os

from django.test import TestCase
import json

from georiviere.portal.validators import validate_json_schema

from georiviere.contribution.tests.factories import (TypePollutionFactory, NaturePollutionFactory,
                                                     FishSpeciesFactory, InvasiveSpeciesFactory, DeadSpeciesFactory,
                                                     HeritageObservationFactory, HeritageSpeciesFactory,
                                                     DiseaseTypeFactory, LandingTypeFactory, SeverityTypeTypeFactory,
                                                     JamTypeFactory)

from georiviere.portal.serializers.contribution import ContributionSchemaSerializer


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
