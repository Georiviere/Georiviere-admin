from collections import OrderedDict

from django.contrib.contenttypes.models import ContentType
from django.urls import reverse
from django.test import TestCase
from geotrek.authent.tests.factories import StructureFactory, UserFactory

from georiviere.finances_administration.models import AdministrativeFile
from georiviere.finances_administration.tests.factories import (AdministrativeFileFactory,
                                                                StudyOperationFactory,
                                                                AdministrativeFilePhaseFactory,
                                                                OrganismFactory)
from georiviere.tests import CommonRiverTest
from georiviere.maintenance.tests.factories import InterventionStatusFactory, InterventionFactory
from georiviere.observations.tests.factories import StationFactory
from georiviere.studies.tests.factories import StudyFactory


class AdministrativePhaseViewTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.administrative_phase = AdministrativeFilePhaseFactory(name="Old name")
        cls.user = UserFactory(password='booh')

    def setUp(self):
        self.client.login(username=self.user.username, password="booh")

    def test_get_update_phase(self):
        response = self.client.get(reverse('finances_administration:administrativephase-update',
                                           kwargs={"pk": self.administrative_phase.pk}),)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Edit phase for', response.content)

    def test_post_update_phase(self):
        self.assertEquals(self.administrative_phase.name, "Old name")
        response = self.client.post(reverse('finances_administration:administrativephase-update',
                                            kwargs={"pk": self.administrative_phase.pk}),
                                    {"name": "New name",
                                     "estimated_budget": 2000,
                                     "administrative_file": self.administrative_phase.administrative_file,
                                     "revised_budget": 200})
        self.assertEqual(response.status_code, 302)
        self.administrative_phase.refresh_from_db()
        self.assertEquals(self.administrative_phase.name, "New name")


class AdministrativeOperationViewTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.administrative_operation = StudyOperationFactory(name="Old name")
        cls.user = UserFactory(password='booh')

    def setUp(self):
        self.client.login(username=self.user.username, password="booh")

    def test_get_update_operation(self):
        response = self.client.get(reverse('finances_administration:administrativeoperation-update',
                                           kwargs={"pk": self.administrative_operation.pk}),)
        self.assertEqual(response.status_code, 200)

    def test_post_update_operation(self):
        self.assertEquals(self.administrative_operation.name, "Old name")
        response = self.client.post(reverse('finances_administration:administrativeoperation-update',
                                            kwargs={"pk": self.administrative_operation.pk}),
                                    {"name": "New name",
                                     "estimated_cost": 2000,
                                     "material_cost": 3000,
                                     "subcontract_cost": 500,

                                     'mandays-TOTAL_FORMS': 0,
                                     'mandays-INITIAL_FORMS': '0',
                                     'mandays-MAX_NUM_FORMS': '',
                                     })
        self.assertEqual(response.status_code, 302)
        self.administrative_operation.refresh_from_db()
        self.assertEquals(self.administrative_operation.name, "New name")


class AdministrativeFileViewTestCase(CommonRiverTest):
    model = AdministrativeFile
    modelfactory = AdministrativeFileFactory

    @classmethod
    def setUpTestData(cls):
        cls.structure = StructureFactory.create()

    def get_expected_json_attrs(self):
        return {
            'id': self.obj.pk,
            'date_insert': '2020-03-17T00:00:00Z',
            'date_update': '2020-03-17T00:00:00Z',
            'description': self.obj.description,
            'structure': self.obj.structure.pk,
            'name': self.obj.name,
            'adminfile_type': self.obj.adminfile_type,
            'domain': self.obj.domain,
            'begin_date': '2010-01-01',
            'end_date': '2012-01-01',
            'constraints': self.obj.constraints,
            'global_cost': '0.00',
            'contractors': [],
            'project_managers': [],
            'project_owners': [],
        }

    def get_bad_data(self):
        return OrderedDict([
            ('name', ''),
            ('begin_date', ''),

            ('operations-TOTAL_FORMS', '0'),
            ('operations-INITIAL_FORMS', '1'),
            ('operations-MAX_NUM_FORMS', '0'),

            ('funding_set-TOTAL_FORMS', '0'),
            ('funding_set-INITIAL_FORMS', '1'),
            ('funding_set-MAX_NUM_FORMS', '0'),

            ('phases-TOTAL_FORMS', '0'),
            ('phases-INITIAL_FORMS', '1'),
            ('phases-MAX_NUM_FORMS', '0'),
        ]), 'This field is required.'

    def get_bad_data_operations(self):
        intervention_object = InterventionFactory.create(
            structure=self.structure
        )
        intervention_contenttype = ContentType.objects.get(model='intervention')
        return {
            'structure': self.structure.pk,
            'name': 'test',
            'adminfile_type': '',
            'domain': '',
            'begin_date': '2010-01-01',
            'end_date': '2012-01-01',
            'constraints': '',
            'global_cost': '12',
            'comments': '',

            'funding_set-TOTAL_FORMS': 0,
            'funding_set-INITIAL_FORMS': '1',
            'funding_set-MAX_NUM_FORMS': '',

            'phases-TOTAL_FORMS': 0,
            'phases-INITIAL_FORMS': '1',
            'phases-MAX_NUM_FORMS': '',

            'operations-TOTAL_FORMS': 3,
            'operations-INITIAL_FORMS': '0',
            'operations-MAX_NUM_FORMS': '',

            'operations-0-id': '',
            'operations-0-name': "",
            'operations-0-content_object': "{}-{}".format(intervention_contenttype.pk, intervention_object.pk),
            'operations-0-operation_status': "",
            'operations-0-estimated_cost': 20000,
            'operations-0-material_cost': 0,
            'operations-0-subcontract_cost': 0,
            'operations-0-DELETE': '',
        }

    def get_bad_data_fundings(self):
        return {
            'structure': self.structure.pk,
            'name': 'test',
            'adminfile_type': '',
            'domain': '',
            'begin_date': '2010-01-01',
            'end_date': '2012-01-01',
            'constraints': '',
            'global_cost': '12',
            'comments': '',

            'funding_set-TOTAL_FORMS': 1,
            'funding_set-INITIAL_FORMS': '0',
            'funding_set-MAX_NUM_FORMS': '',

            'funding_set-0-id': '',
            'funding_set-0-amount': 20000,
            'funding_set-0-organism': '',
            'funding_set-0-DELETE': '',

            'phases-TOTAL_FORMS': 0,
            'phases-INITIAL_FORMS': '1',
            'phases-MAX_NUM_FORMS': '',

            'operations-TOTAL_FORMS': 0,
            'operations-INITIAL_FORMS': '1',
            'operations-MAX_NUM_FORMS': '',
        }

    def get_bad_data_phases(self):
        return {
            'structure': self.structure.pk,
            'name': 'test',
            'adminfile_type': '',
            'domain': '',
            'begin_date': '2010-01-01',
            'end_date': '2012-01-01',
            'constraints': '',
            'global_cost': '12',
            'comments': '',

            'funding_set-TOTAL_FORMS': 0,
            'funding_set-INITIAL_FORMS': '1',
            'funding_set-MAX_NUM_FORMS': '',

            'phases-TOTAL_FORMS': 1,
            'phases-INITIAL_FORMS': '0',
            'phases-MAX_NUM_FORMS': '',

            'phases-0-id': '',
            'phases-0-name': '',
            'phases-0-estimated_budget': "wrong value",
            'phases-0-revised_budget': 0,
            'phases-0-DELETE': '',

            'operations-TOTAL_FORMS': 0,
            'operations-INITIAL_FORMS': '1',
            'operations-MAX_NUM_FORMS': '',
        }

    def get_good_data(self):
        organism1 = OrganismFactory.create()
        organism2 = OrganismFactory.create()

        return {
            'structure': self.structure.pk,
            'name': 'test',
            'adminfile_type': '',
            'domain': '',
            'begin_date': '2010-01-01',
            'end_date': '2012-01-01',
            'constraints': '',
            'global_cost': '12',
            'comments': '',
            'contractors': organism2.pk,
            'project_owners': organism1.pk,
            'project_managers': organism2.pk,

            'funding_set-TOTAL_FORMS': 0,
            'funding_set-INITIAL_FORMS': '0',
            'funding_set-MAX_NUM_FORMS': '',

            'phases-TOTAL_FORMS': 0,
            'phases-INITIAL_FORMS': '0',
            'phases-MAX_NUM_FORMS': '',

            'operations-TOTAL_FORMS': 0,
            'operations-INITIAL_FORMS': '0',
            'operations-MAX_NUM_FORMS': '',

        }

    def get_good_data_with_fundings(self):
        """Create a Study and a Station with same structure as AdministrativeFile"""
        organism1 = OrganismFactory.create()
        organism2 = OrganismFactory.create()

        return {
            'structure': self.structure.pk,
            'name': 'test',
            'adminfile_type': '',
            'domain': '',
            'begin_date': '2010-01-01',
            'end_date': '2012-01-01',
            'constraints': '',
            'global_cost': '12',
            'comments': '',
            'contractors': organism2.pk,
            'project_owners': organism1.pk,
            'project_managers': organism2.pk,

            'funding_set-TOTAL_FORMS': 2,
            'funding_set-INITIAL_FORMS': '0',
            'funding_set-MAX_NUM_FORMS': '',

            'funding_set-0-id': '',
            'funding_set-0-amount': 20000,
            'funding_set-0-organism': organism1.pk,
            'funding_set-0-DELETE': '',

            'funding_set-1-id': '',
            'funding_set-1-amount': 10000,
            'funding_set-1-organism': organism2.pk,
            'funding_set-1-DELETE': '',

            'operations-TOTAL_FORMS': 0,
            'operations-INITIAL_FORMS': '0',
            'operations-MAX_NUM_FORMS': '',

            'phases-TOTAL_FORMS': 0,
            'phases-INITIAL_FORMS': '0',
            'phases-MAX_NUM_FORMS': '',
        }

    def get_good_data_with_operations(self):
        """Create a Study and a Station with same structure as AdministrativeFile"""
        organism1 = OrganismFactory.create()
        organism2 = OrganismFactory.create()
        study_object = StudyFactory.create(
            structure=self.structure
        )
        station_object = StationFactory.create(
            structure=self.structure
        )
        intervention_object = InterventionFactory.create(
            structure=self.structure
        )
        study_contenttype = ContentType.objects.get(model='study')
        station_contenttype = ContentType.objects.get(model='station')
        intervention_contenttype = ContentType.objects.get(model='intervention')
        status = InterventionStatusFactory.create()

        return {
            'structure': self.structure.pk,
            'name': 'test',
            'adminfile_type': '',
            'domain': '',
            'begin_date': '2010-01-01',
            'end_date': '2012-01-01',
            'constraints': '',
            'global_cost': '12',
            'comments': '',
            'contractors': organism2.pk,
            'project_owners': organism1.pk,
            'project_managers': organism2.pk,

            'funding_set-TOTAL_FORMS': 0,
            'funding_set-INITIAL_FORMS': '0',
            'funding_set-MAX_NUM_FORMS': '',

            'phases-TOTAL_FORMS': 0,
            'phases-INITIAL_FORMS': '0',
            'phases-MAX_NUM_FORMS': '',

            'operations-TOTAL_FORMS': 3,
            'operations-INITIAL_FORMS': '0',
            'operations-MAX_NUM_FORMS': '',

            'operations-0-id': '',
            'operations-0-name': "Operation",
            'operations-0-content_object': "{}-{}".format(study_contenttype.pk, study_object.pk),
            'operations-0-operation_status': status.pk,
            'operations-0-estimated_cost': 20000,
            'operations-0-material_cost': 0,
            'operations-0-subcontract_cost': 0,
            'operations-0-DELETE': '',

            'operations-1-id': '',
            'operations-1-name': "Operation",
            'operations-1-content_object': "{}-{}".format(station_contenttype.pk, station_object.pk),
            'operations-1-operation_status': '',
            'operations-1-estimated_cost': 0,
            'operations-1-material_cost': 0,
            'operations-1-subcontract_cost': 0,
            'operations-1-DELETE': '',

            'operations-2-id': '',
            'operations-2-name': "Operation",
            'operations-2-content_object': "{}-{}".format(intervention_contenttype.pk, intervention_object.pk),
            'operations-2-operation_status': '',
            'operations-2-estimated_cost': 0,
            'operations-2-material_cost': 0,
            'operations-2-subcontract_cost': 0,
            'operations-2-DELETE': '',
        }

    def get_good_data_with_phases(self):
        """Create a Study and a Station with same structure as AdministrativeFile"""
        organism1 = OrganismFactory.create()
        organism2 = OrganismFactory.create()

        return {
            'structure': self.structure.pk,
            'name': 'test',
            'adminfile_type': '',
            'domain': '',
            'begin_date': '2010-01-01',
            'end_date': '2012-01-01',
            'constraints': '',
            'global_cost': '12',
            'comments': '',
            'contractors': organism2.pk,
            'project_owners': organism1.pk,
            'project_managers': organism2.pk,

            'funding_set-TOTAL_FORMS': 0,
            'funding_set-INITIAL_FORMS': '0',
            'funding_set-MAX_NUM_FORMS': '',

            'operations-TOTAL_FORMS': 0,
            'operations-INITIAL_FORMS': '0',
            'operations-MAX_NUM_FORMS': '',

            'phases-TOTAL_FORMS': 3,
            'phases-INITIAL_FORMS': '0',
            'phases-MAX_NUM_FORMS': '',

            'phases-0-id': '',
            'phases-0-name': "Phase 1",
            'phases-0-estimated_budget': 20000,
            'phases-0-revised_budget': 0,
            'phases-0-DELETE': '',

            'phases-1-id': '',
            'phases-1-name': "Phase 2",
            'phases-1-estimated_budget': 0,
            'phases-1-revised_budget': 0,
            'phases-1-DELETE': '',

            'phases-2-id': '',
            'phases-2-name': "Phase 3",
            'phases-2-estimated_budget': 0,
            'phases-2-revised_budget': 500,
            'phases-2-DELETE': '',
        }

    def _check_update_geom_permission(self, response):
        """Pass check geom permission, AdministrativeFile has no geom"""
        pass

    def test_crud_with_operations(self):
        self.login()
        response = self.client.post(self._get_add_url(), self.get_good_data_with_operations())
        self.assertEqual(response.status_code, 302)
        administrative_file = self.model.objects.last()
        self.assertEquals(administrative_file.operations.count(), 3)
        response = self.client.post(self._get_add_url(), self.get_bad_data_operations())
        self.assertEqual(response.status_code, 200)
        self.assertEquals(administrative_file.operations.count(), 3)

    def test_crud_with_fundings(self):
        self.login()
        response = self.client.post(self._get_add_url(), self.get_good_data_with_fundings())
        self.assertEqual(response.status_code, 302)
        administrative_file = self.model.objects.last()
        self.assertEquals(administrative_file.funding_set.count(), 2)
        self.assertEquals(administrative_file.funders.count(), 2)
        response = self.client.post(self._get_add_url(), self.get_bad_data_fundings())
        self.assertEqual(response.status_code, 200)
        self.assertEquals(administrative_file.funders.count(), 2)

    def test_crud_with_phases(self):
        self.login()
        response = self.client.post(self._get_add_url(), self.get_good_data_with_phases())
        self.assertEqual(response.status_code, 302)
        administrative_file = self.model.objects.last()
        self.assertEquals(administrative_file.phases.count(), 3)
        response = self.client.post(self._get_add_url(), self.get_bad_data_phases())
        self.assertEqual(response.status_code, 200)
        self.assertEquals(administrative_file.phases.count(), 3)
