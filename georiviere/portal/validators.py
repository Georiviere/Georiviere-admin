from django.core.exceptions import ValidationError
from jsonschema.validators import validator_for


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
