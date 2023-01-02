from copy import deepcopy

from geotrek.authent.models import default_structure
from geotrek.common.mixins.forms import WithStructureFormMixin
from mapentity.forms import MapEntityForm


class CommonForm(WithStructureFormMixin, MapEntityForm):
    """Common GeoRivière form"""

    def __init__(self, *args, **kwargs):

        self.fieldslayout = deepcopy(self.fieldslayout)
        super().__init__(*args, **kwargs)
        self.fields = self.fields.copy()
        self.update = kwargs.get("instance") is not None
        if 'structure' in self.fields:
            self.initialize_fields_with_structure()

    def save(self, commit=True):
        """Set structure field before saving if need be"""
        if self.update:  # Structure is already set on object.
            pass
        elif not hasattr(self.instance, 'structure'):
            pass
        elif 'structure' in self.fields:
            pass  # The form contains the structure field. Let django use its value.
        elif self.user:
            self.instance.structure = self.user.profile.structure
        else:
            self.instance.structure = default_structure()
        return super().save(commit)
