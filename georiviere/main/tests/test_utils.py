from django.test import TestCase
from django.utils import translation

from georiviere.main.utils import simplify_coords


class SimplifyCordsTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        translation.deactivate()
        cls.coords = [0.0, 1.8888882222]
        cls.fail_coords = 'test'

    def test_simplify_coords(self):
        coords_simplified = simplify_coords(coords=self.coords)
        self.assertEqual(coords_simplified, [0.0, 1.8888882])

    def test_simplify_coords_fail(self):
        with self.assertRaisesRegex(Exception, "Param is <class 'str'>. Should be <list>, <tuple> or <float>"):
            simplify_coords(coords=self.fail_coords)
