from django.test import TestCase

from watershed import factories


class StationTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.watershed_type = factories.WatershedTypeFactory(name="Toto")
        cls.watershed = factories.WatershedFactory(name="Tata", watershed_type=cls.watershed_type)

    def test_watershed_str(self):
        self.assertEqual(str(self.watershed), 'Toto - Tata')

    def test_watershed_type_str(self):
        self.assertEqual(str(self.watershed_type), 'Toto')
