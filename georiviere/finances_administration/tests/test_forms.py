from django.test import TestCase

from georiviere.studies.tests.factories import StudyFactory
from . import factories


class AdministrativeFileTest(TestCase):

    @classmethod
    def setUpTestData(cls):

        cls.admin_file1 = factories.AdministrativeFileFactory(
            name="Hello goodbye",
        )
        cls.study1 = StudyFactory.create(
            title="Étude de cas"
        )
        cls.operation_study = factories.StudyOperationFactory(
            content_object=cls.study1,
            administrative_file=cls.admin_file2,
            estimated_cost=10000,
            material_cost=2000,
            subcontract_cost=9000,
        )
        cls.job_cat1 = factories.JobCategoryFactory(man_day_cost=500)

        cls.mandays1 = factories.ManDayFactory.create(
            job_category=cls.job_cat1,
            operation=cls.operation_study,
            nb_days=5
        )

    def manday_in_administrative_file_form(self):
        self.login()
        response = self.client.get(self.admin_file1.get_update_url())
        self.assertContains(response, "<div>2500.00</div>")
