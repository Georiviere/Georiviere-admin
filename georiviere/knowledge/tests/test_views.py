from collections import OrderedDict

from django.core.exceptions import ObjectDoesNotExist
from geotrek.authent.factories import StructureFactory

from georiviere.tests import CommonRiverTest
from . import factories
from ..models import Knowledge, Vegetation, Work, FollowUp


class KnowledgeViewTestCase(CommonRiverTest):
    model = Knowledge
    modelfactory = factories.KnowledgeFactory
    fixtures = ['georiviere/knowledge/fixtures/basic.json']

    def get_expected_json_attrs(self):
        return {
            'id': self.obj.pk,
            'code': self.obj.code,
            'date_insert': '2020-03-17T00:00:00Z',
            'date_update': '2020-03-17T00:00:00Z',
            'description': self.obj.description,
            'geom': self.obj.geom.ewkt,
            'name': self.obj.name,
            'structure': self.obj.structure.pk,
            'knowledge_type': self.obj.knowledge_type.pk
        }

    def get_bad_data(self):
        return OrderedDict([
            ('name', ''),
        ]), 'This field is required.'

    def get_good_data(self):
        structure = StructureFactory.create()
        knowledge_type = factories.KnowledgeTypeFactory.create()
        temp_data = self.modelfactory.build(
            structure=structure,
        )
        return {
            'structure': structure.pk,
            'geom': temp_data.geom.ewkt,
            'knowledge_type': knowledge_type.pk,
            'code': '1234',
            'name': 'test',
            'description': 'This is a description',
        }

    def test_whatevertype_knowledge_create(self):
        """Create a knowledge whatever type, and another vegetation type"""

        self.login()
        good_data = self.get_good_data()
        good_data['name'] = "No vegetation related"
        good_data['knowledge_type'] = factories.KnowledgeTypeFactory.create(label="Something").pk
        self.client.post(self._get_add_url(), good_data)

        knowledge_created = Knowledge.objects.get(name="No vegetation related")
        with self.assertRaises(ObjectDoesNotExist):
            knowledge_created.vegetation
            knowledge_created.work

    def test_worktype_knowledge_create_update(self):
        """Create a knowledge work type, then update it"""

        self.login()
        good_data = self.get_good_data()
        good_data['name'] = "With work related"
        good_data['knowledge_type'] = 2
        good_data['work_type'] = factories.WorkTypeFactory.create().pk
        good_data['material'] = factories.WorkMaterialFactory.create().pk

        # Create a knowledge work type with data for work form
        self.client.post(self._get_add_url(), good_data)
        knowledge_created = Knowledge.objects.filter(name="With work related")
        self.assertEquals(knowledge_created.count(), 1)
        self.assertIsInstance(knowledge_created[0].work, Work)

        # Update it
        good_data['work_type'] = factories.WorkTypeFactory.create().pk
        self.client.post(knowledge_created[0].get_update_url(), good_data)
        self.assertEquals(knowledge_created[0].work.work_type.pk, good_data['work_type'])

    def test_vegetationtype_knowledge_create_update(self):
        """Create a knowledge vegetation type, then update it"""

        self.login()
        good_data = self.get_good_data()

        good_data['name'] = "With vegetation related"
        good_data['knowledge_type'] = 1
        good_data['vegetation_type'] = factories.VegetationTypeFactory.create().pk

        # Create a knowledge vegetation type with data for vegetation form
        self.client.post(self._get_add_url(), good_data)
        knowledge_created = Knowledge.objects.filter(name="With vegetation related")
        self.assertEquals(knowledge_created.count(), 1)
        self.assertIsInstance(knowledge_created[0].vegetation, Vegetation)

        # Update it
        good_data['vegetation_type'] = factories.VegetationTypeFactory.create().pk
        self.client.post(knowledge_created[0].get_update_url(), good_data)
        self.assertEquals(knowledge_created[0].vegetation.vegetation_type.pk, good_data['vegetation_type'])

    def test_vegetationtype_knowledge_create_baddata(self):
        """Create a knowledge vegetation type, then update it"""

        self.login()
        bad_data = self.get_good_data()

        bad_data['name'] = "With vegetation related but bad data"
        bad_data['knowledge_type'] = 1

        # Try to create a knowledge vegetation type with data for vegetation form
        response = self.client.post(self._get_add_url(), bad_data)
        self.assertFalse(response.context_data['vegetation_form'].is_valid())

        knowledges = Knowledge.objects.filter(name="With vegetation related but bad data")
        self.assertEquals(knowledges.count(), 0)

    def test_worktype_knowledge_create_baddata(self):
        """Create a knowledge vegetation type, then update it"""

        self.login()
        bad_data = self.get_good_data()

        bad_data['name'] = "With work related but bad data"
        bad_data['knowledge_type'] = 2

        # Try to create a knowledge vegetation type with data for vegetation form
        response = self.client.post(self._get_add_url(), bad_data)
        self.assertFalse(response.context_data['work_form'].is_valid())

        knowledges = Knowledge.objects.filter(name="With work related but bad data")
        self.assertEquals(knowledges.count(), 0)

    def test_listing_number_queries(self):
        """Test number queries when get list object"""
        self.login()
        self.modelfactory.create_batch(100)

        with self.assertNumQueries(30):
            self.client.get(self.model.get_list_url())

        with self.assertNumQueries(6):
            self.client.get(self.model.get_jsonlist_url())

        with self.assertNumQueries(5):
            self.client.get(self.model.get_format_list_url())

    def test_detail_number_queries(self):
        """Test number queries when get detail object"""
        self.login()
        station = self.modelfactory.create()

        with self.assertNumQueries(41):
            self.client.get(station.get_detail_url())


class FollowUpViewsTest(CommonRiverTest):
    model = FollowUp
    modelfactory = factories.FollowUpKnowledgeFactory

    def get_expected_json_attrs(self):
        return {
            'id': self.obj.pk,
            'description': self.obj.description,
            'name': self.obj.name,
            'width': 0.0,
            'height': 0.0,
            'length': 0.0,
            'followup_type': self.obj.followup_type.pk,
        }

    def get_bad_data(self):
        return OrderedDict([
            ('name', ''),
            ('structure', ''),
        ]), 'This field is required.'

    def get_good_data(self):
        structure = StructureFactory.create()
        good_data = {
            'structure': structure.pk,
            'name': 'test',
            'date': '2012-08-23',
            'description': '',
            'height': 0.0,
            'width': 0.0,
            'length': 0.0,
            'followup_type': factories.FollowUpTypeFactory.create().pk,
        }
        return good_data

    def test_listing_number_queries(self):
        """Test number queries when get list object"""
        self.login()
        self.modelfactory.create_batch(100)

        with self.assertNumQueries(32):
            self.client.get(self.model.get_list_url())

        with self.assertNumQueries(6):
            self.client.get(self.model.get_jsonlist_url())

        with self.assertNumQueries(5):
            self.client.get(self.model.get_format_list_url())

    def test_detail_number_queries(self):
        """Test number queries when get detail object"""
        self.login()
        station = self.modelfactory.create()

        with self.assertNumQueries(41):
            self.client.get(station.get_detail_url())
