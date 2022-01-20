from django.utils.translation import gettext_lazy as _

from crispy_forms.layout import Div, Field
from crispy_forms.bootstrap import AppendedText
from dal import autocomplete
from geotrek.common.forms import CommonForm

from georiviere.knowledge.models import Knowledge
from georiviere.main.widgets import DatePickerInput
from georiviere.maintenance.models import Intervention
from georiviere.river.fields import SnappedGeometryField


class InterventionForm(autocomplete.FutureModelForm, CommonForm):
    """Intervention form"""
    _geom = SnappedGeometryField(required=False)

    geomfields = ['_geom']

    target = autocomplete.Select2GenericForeignKeyModelField(
        model_choice=[
            (Knowledge, 'name')
        ],
        label=_('Knowledge'),
        required=False,
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
            "disorders",
            "description",
            AppendedText("length", "m"),
            AppendedText("width", "m"),
            AppendedText("height", "m"),
        )]

    class Meta:
        model = Intervention
        fields = [
            "structure", "target", "name", "date",
            "intervention_status", "intervention_type",
            "stake", "disorders", "description",
            "length", "width", "height", "_geom"
        ]
        widgets = {
            'date': DatePickerInput(),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper.form_tag = False
