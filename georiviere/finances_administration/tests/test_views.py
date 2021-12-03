from collections import OrderedDict

from django.contrib.contenttypes.models import ContentType
from geotrek.authent.tests.factories import StructureFactory

from georiviere.finances_administration.models import AdministrativeFile
from georiviere.finances_administration.tests.factories import AdministrativeFileFactory, OrganismFactory
from georiviere.tests import CommonRiverTest
from georiviere.maintenance.tests.factories import InterventionStatusFactory, InterventionFactory
from georiviere.observations.tests.factories import StationFactory
from georiviere.studies.tests.factories import StudyFactory


class AdministrativeFileViewTestCase(CommonRiverTest):
    model = AdministrativeFile
    modelfactory = AdministrativeFileFactory

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
        ]), 'This field is required.'

    def get_good_data(self):
        structure = StructureFactory.create()
        organism1 = OrganismFactory.create()
        organism2 = OrganismFactory.create()

        return {
            'structure': structure.pk,
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

        }

    def get_good_data_with_fundings(self):
        """Create a Study and a Station with same structure as AdministrativeFile"""
        structure = StructureFactory.create()
        organism1 = OrganismFactory.create()
        organism2 = OrganismFactory.create()

        return {
            'structure': structure.pk,
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

        }

    def get_good_data_with_operations(self):
        """Create a Study and a Station with same structure as AdministrativeFile"""
        structure = StructureFactory.create()
        organism1 = OrganismFactory.create()
        organism2 = OrganismFactory.create()
        study_object = StudyFactory.create(
            structure=structure
        )
        station_object = StationFactory.create(
            structure=structure
        )
        intervention_object = InterventionFactory.create(
            structure=structure
        )
        study_contenttype = ContentType.objects.get(model='study')
        station_contenttype = ContentType.objects.get(model='station')
        intervention_contenttype = ContentType.objects.get(model='intervention')
        status = InterventionStatusFactory.create()

        return {
            'structure': structure.pk,
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

    def _check_update_geom_permission(self, response):
        """Pass check geom permission, AdministrativeFile has no geom"""
        pass

    def test_crud_with_operations(self):
        self.login()
        response = self.client.post(self._get_add_url(), self.get_good_data_with_operations())
        self.assertEqual(response.status_code, 302)
        administrative_file = self.model.objects.last()
        self.assertEquals(administrative_file.operations.count(), 3)

    def test_crud_with_fundings(self):
        self.login()
        response = self.client.post(self._get_add_url(), self.get_good_data_with_fundings())
        self.assertEqual(response.status_code, 302)
        administrative_file = self.model.objects.last()
        self.assertEquals(administrative_file.funding_set.count(), 2)
        self.assertEquals(administrative_file.funders.count(), 2)
