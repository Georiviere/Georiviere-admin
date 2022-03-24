from django.test import TestCase

from .factories import DataSourceFactory


class DataSourceTest(TestCase):

    def test_str(self):
        data_source = DataSourceFactory(name="Jouvence")
        self.assertEqual(str(data_source), "Jouvence")
