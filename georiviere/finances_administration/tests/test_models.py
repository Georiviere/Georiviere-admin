from django.contrib.gis.geos import GeometryCollection
from django.test import TestCase
from geotrek.authent.factories import StructureFactory

from georiviere.observations.tests.factories import StationFactory
from georiviere.studies.tests.factories import StudyFactory
from . import factories


class AdministrativeFileTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.structure = StructureFactory(
            name="Ma structure"
        )
        cls.organism1 = factories.OrganismFactory(
            name="Ma petite entreprise"
        )
        cls.organism2 = factories.OrganismFactory(
            name="Ma petite entreprise 2",
            structure=cls.structure
        )
        cls.admin_file_type = factories.AdministrativeFileTypeFactory(
            label="Rubrique à brac",
            structure=cls.structure
        )
        cls.admin_file_domain = factories.AdministrativeFileDomainFactory(
            label="Domaine public",
            structure=cls.structure
        )
        cls.admin_file1 = factories.AdministrativeFileFactory(
            name="Hello goodbye",
        )
        cls.admin_file2 = factories.AdministrativeFileFactory(
            name="Hello goodbye",
        )
        cls.study1 = StudyFactory.create(
            title="Étude de cas"
        )
        cls.station1 = StationFactory.create(
            label="Station verticale"
        )
        cls.operation_study = factories.StudyOperationFactory(
            content_object=cls.study1,
            administrative_file=cls.admin_file2,
            estimated_cost=10000,
            material_cost=2000,
            subcontract_cost=9000,
        )
        cls.operation_station1 = factories.StationOperationFactory(
            content_object=cls.station1,
            administrative_file=cls.admin_file1,
            estimated_cost=12000,
            material_cost=3000,
            subcontract_cost=5000,
        )
        cls.operation_station2 = factories.StationOperationFactory(
            content_object=cls.station1,
            administrative_file=cls.admin_file2,
            estimated_cost=18000,
            material_cost=4000,
            subcontract_cost=15000,
        )
        cls.funding1 = factories.FundingFactory(
            organism=cls.organism1,
            administrative_file=cls.admin_file1
        )
        cls.funding2 = factories.FundingFactory(
            organism=cls.organism2,
            administrative_file=cls.admin_file1
        )
        cls.job_cat1 = factories.JobCategoryFactory(man_day_cost=500)
        cls.job_cat2 = factories.JobCategoryFactory(man_day_cost=700)

    def test_str(self):
        self.assertEqual(str(self.admin_file1), "Hello goodbye")

    def test_str_with_structure(self):
        """Test str methods for objects with structure or None"""
        self.assertEqual(str(self.organism1), "Ma petite entreprise")
        self.assertEqual(str(self.organism2), "Ma petite entreprise 2 (Ma structure)")
        self.assertEqual(str(self.admin_file_type), "Rubrique à brac (Ma structure)")
        self.assertEqual(str(self.admin_file_domain), "Domaine public (Ma structure)")

    def test_funders_display(self):
        """Test funders display method for AdministrativeFile"""
        self.assertEqual(self.admin_file1.funders_display,
                         ["Ma petite entreprise", "Ma petite entreprise 2 (Ma structure)"])

    def test_create_project_operations(self):
        """Test when operations are set to an AdministrativeFile
        administrative file geom"""
        self.assertTrue(self.admin_file2.geom.equals(GeometryCollection(self.study1.geom.union(self.station1.geom))))

    def test_mandays(self):
        """Test man-day cost for an operation"""

        self.mandays1 = factories.ManDayFactory.create(
            job_category=self.job_cat1,
            operation=self.operation_station1,
            nb_days=5
        )
        self.mandays2 = factories.ManDayFactory.create(
            job_category=self.job_cat2,
            operation=self.operation_station1,
            nb_days=8
        )
        manday_total_costs = 5 * 500 + 8 * 700
        self.assertEqual(self.operation_station1.manday_cost, manday_total_costs)

    def test_total_costs(self):
        """Test computed costs for an AdministrativeFile with operations with costs"""
        self.assertEqual(self.operation_study.actual_cost, 11000)
        admin_file2_computed_costs = self.admin_file2.total_costs
        self.assertEqual(admin_file2_computed_costs['actual'], 30000)
        self.assertEqual(admin_file2_computed_costs['estimated'], 28000)

    def test_costs_mandays(self):
        """Test computed costs for an AdministrativeFile with operations with mandays costs"""
        self.mandays = factories.ManDayFactory.create(
            job_category=self.job_cat1,
            operation=self.operation_station2,
            nb_days=2
        )
        operation_total_costs = 19000 + 2 * 500
        self.assertEqual(self.operation_station2.actual_cost, operation_total_costs)
        admin_file2_total_costs = self.admin_file2.total_costs
        self.assertEqual(admin_file2_total_costs['actual'], 31000)
