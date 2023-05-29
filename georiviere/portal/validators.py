from django.core.exceptions import ValidationError
from jsonschema.validators import validator_for
import jsonschema


def validate_json_schema(value):
    """
    Validate json schema
    """
    try:
        if value:
            # check only if schema defined
            cls = validator_for(value)
            cls.check_schema(value)
    except Exception as e:
        raise ValidationError(message=e.message)

    return value


def validate_json_schema_data(value, schema):
    """
    Validate data according json schema
    """
    try:
        # TODO: check additional value properties and all of properties
        if value and schema:
            jsonschema.validators.validate(value, schema)
    except jsonschema.exceptions.ValidationError as e:
        raise ValidationError(message=e.message)
    return value
