from django.core.exceptions import ValidationError
from django.test import TestCase

from georiviere.description.tests import factories
from georiviere.river.tests.factories import TopologyFactory


class DescriptionTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.usage_type = factories.UsageTypeFactory.create()
        cls.usage_type_2 = factories.UsageTypeFactory.create()
        cls.usage = factories.UsageFactory.create(usage_types=[cls.usage_type, cls.usage_type_2])

    def test_str(self):
        self.assertEqual(str(self.usage), "Usage type 0, Usage type 1")


class StatusTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.status_type = factories.StatusTypeFactory.create()
        cls.status_type_2 = factories.StatusTypeFactory.create()
        cls.status = factories.StatusFactory.create(status_types=[cls.status_type, cls.status_type_2])

    def test_status_clean(self):
        """
        Check status can't be qualified without type
        """
        topology = TopologyFactory.create(qualified=True)
        status = factories.StatusFactory.create(topology=topology)
        with self.assertRaises(ValidationError):
            status.clean()

    def test_str(self):
        self.assertEqual(str(self.status), "Status type 0, Status type 1")


class MorphologyTest(TestCase):
    def test_planlayout_str(self):
        plan_layout_type = factories.PlanLayoutTypeFactory.create()
        self.assertEqual(str(plan_layout_type), "Plan layout type 0")

    def test_habitattype_str(self):
        habitat_type = factories.HabitatTypeFactory.create()
        self.assertEqual(str(habitat_type), "Habitat type 0")

    def test_habitatsdiversity_str(self):
        habitats_diversity = factories.HabitatsDiversityFactory.create()
        self.assertEqual(str(habitats_diversity), "Habitats diversity 0")

    def test_bankstate_str(self):
        bank_state = factories.BankStateFactory.create()
        self.assertEqual(str(bank_state), "Bank state 0")

    def test_sedimentdynamic_str(self):
        sediment_dynamic = factories.SedimentDynamicFactory.create()
        self.assertEqual(str(sediment_dynamic), "Sediment dynamic 0")

    def test_granulometricdiversity_str(self):
        granulometric_diversity = factories.GranulometricDiversityFactory.create()
        self.assertEqual(str(granulometric_diversity), "Granulometric diversity 0")

    def test_faciesdiversity_str(self):
        facies_diversity = factories.FaciesDiversityFactory.create()
        self.assertEqual(str(facies_diversity), "Facies diversity 0")

    def test_workingspacetype_str(self):
        working_space_type = factories.WorkingSpaceTypeFactory.create()
        self.assertEqual(str(working_space_type), "Working space type 0")

    def test_flowtype_str(self):
        flow_type = factories.FlowTypeFactory.create()
        self.assertEqual(str(flow_type), "Flow type 0")
