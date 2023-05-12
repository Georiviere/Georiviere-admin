from django.core.exceptions import ValidationError
from django.test import TestCase

from georiviere.portal.validators import validate_bounds


class PortalTest(TestCase):
    def test_empty(self):
        value = ""
        self.assertIsNone(validate_bounds(value))

    def test_dict(self):
        value = "{'test': []}"
        with self.assertRaisesRegexp(ValidationError, "{'test': []} is not a bound it should be like : [a, b, c, d]"):
            validate_bounds(value)

    def test_list_not_bounds(self):
        value = "[0, 1, 2]"

        with self.assertRaises(ValidationError):
            validate_bounds(value)

    def test_bounds(self):
        value = "[0, 1, 2, 3]"
        self.assertIsNone(validate_bounds(value))
