from django.test import TestCase
from geotrek.authent.tests.factories import StructureFactory

from .factories import DataSourceFactory


class DataSourceTest(TestCase):
    """Test for Data source model"""

    def test_str(self):
        data_source = DataSourceFactory(name="Jouvence")
        self.assertEqual(str(data_source), "Jouvence")

        data_source.structure = StructureFactory(name="Ma petite entreprise")
        data_source.save()
        self.assertEqual(str(data_source), "Jouvence (Ma petite entreprise)")
