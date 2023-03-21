from django.utils.translation import gettext_lazy as _

from crispy_forms.layout import Div, Field
from crispy_forms.bootstrap import AppendedText
from dal import autocomplete
from geotrek.common.forms import CommonForm

from georiviere.finances_administration.forms import AdministrativeFileObjectFormMixin
from georiviere.knowledge.models import Knowledge
from georiviere.main.widgets import DatePickerInput
from georiviere.maintenance.models import Intervention
from georiviere.river.fields import SnappedGeometryField


class InterventionForm(AdministrativeFileObjectFormMixin, CommonForm):
    """Intervention form"""
    _geom = SnappedGeometryField(required=False)

    geomfields = ['_geom']

    target = autocomplete.Select2GenericForeignKeyModelField(
        model_choice=[
            (Knowledge, 'name')
        ],
        label=_('Knowledge'),
        required=False,
        initial=None,
    )

    fieldslayout = [
        Div(
            "structure",
            Field('target', css_class="chosen-select"),
            "name",
            "date",
            "intervention_status",
            "intervention_type",
            "stake",
            Field('disorders', css_class="chzn-select"),
            "description",
            AppendedText("length", "m"),
            AppendedText("width", "m"),
            AppendedText("height", "m"),
            Div(css_id="div_id_operations", css_class="form-group row"),
            "administrative_file",
        )]

    class Meta:
        model = Intervention
        fields = [
            "structure", "target", "name", "date",
            "intervention_status", "intervention_type",
            "stake", "disorders", "description",
            "length", "width", "height", "_geom", "administrative_file"
        ]
        widgets = {
            'date': DatePickerInput(),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper.form_tag = False

    def clean_target(self):
        target = self.cleaned_data['target']
        if target == "":
            return None
        return target
