from django.test import TestCase

from .factories import POITypeFactory, POICategoryFactory

from geotrek.authent.tests.factories import StructureFactory


class AdministrativeFileTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.structure = StructureFactory.create(
            name="foo_structure"
        )
        cls.poi_type = POITypeFactory.create(label="foo")
        cls.poi_type_structure = POITypeFactory.create(label="bar", structure=cls.structure)
        cls.poi_category = POICategoryFactory.create(label="fof")
        cls.poi_category_structure = POICategoryFactory.create(label="baf", structure=cls.structure)

    def test_str_poi_type(self):
        self.assertEqual(str(self.poi_type), 'foo')
        self.assertEqual(str(self.poi_type_structure), 'bar (foo_structure)')

    def test_str_poi_category(self):
        self.assertEqual(str(self.poi_category), 'fof')
        self.assertEqual(str(self.poi_category_structure), 'baf (foo_structure)')
