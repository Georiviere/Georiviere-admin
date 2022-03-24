from django.test import TestCase

from ..models import DataSource


class DataSourceTest(TestCase):

    def test_str(self):
        data_source = DataSource(name="Jouvence")
        self.assertEqual(str(data_source), "Jouvence")
