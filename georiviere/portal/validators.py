import json

from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


def validate_bounds(value):
    try:
        if value:
            bounds = json.loads(value)
            if not isinstance(bounds, list):
                raise ValidationError(
                    _("%(value)s is not a bound it should be like : [a, b, c, d]"),
                    params={"value": value},
                )
            if len(bounds) != 4:
                raise ValidationError(
                    _("%(value)s is not a bound it should be like : [a, b, c, d]"),
                    params={"value": value},
                )
    except json.JSONDecodeError:
        raise ValidationError(
            _("%(value)s is not a bound it should be like : [a, b, c, d]"),
            params={"value": value},
        )
