from django.core.exceptions import ValidationError
from django.test import TestCase

from georiviere.portal.validators import validate_json_schema, validate_json_schema_data

bad_json_schema = {
    "type": "object",
    "required": [
        1
    ],
    "properties": {
        "name_author": {
            "type": "string",
            "title": "Name author"
        }
    }
}

good_json_schema = {
    "type": "object",
    "properties": {
        "name_author": {
            "type": "string",
            "title": "Name author"
        }
    },
    "required": ["name_author"]
}


class ValidateJSONSchemaTestCase(TestCase):
    def test_validator_with_wrong_jsonschema(self):
        with self.assertRaises(ValidationError):
            validate_json_schema(bad_json_schema)

    def test_validator_jsonschema(self):
        self.assertEqual(good_json_schema, validate_json_schema(good_json_schema))


class ValidateJSONSchemaDataTestCase(TestCase):
    def test_validator_jsonschema_data(self):
        self.assertEqual({"name_author": "foo"}, validate_json_schema_data({"name_author": "foo"}, good_json_schema))

    def test_validator_jsonschema_data_fail(self):
        with self.assertRaisesRegexp(ValidationError, """["'name_author' is a required property"]"""):
            validate_json_schema_data({}, good_json_schema)
