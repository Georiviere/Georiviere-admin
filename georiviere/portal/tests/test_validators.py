from django.core.exceptions import ValidationError
from django.test import TestCase

from georiviere.portal.validators import validate_json_schema

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
    }
}


class ValidateJSONSchemaTestCase(TestCase):
    def test_validator_with_wrong_jsonschema(self):
        with self.assertRaises(ValidationError):
            validate_json_schema(bad_json_schema)

    def test_validator_jsonschema(self):
        self.assertEqual(good_json_schema, validate_json_schema(good_json_schema))
