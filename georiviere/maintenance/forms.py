from django.utils.translation import gettext_lazy as _

from crispy_forms.layout import Div, Field
from dal import autocomplete
from geotrek.common.forms import CommonForm

from georiviere.knowledge.models import Knowledge
from georiviere.main.widgets import DatePickerInput
from georiviere.maintenance.models import Intervention
from georiviere.observations.models import Station


class InterventionForm(autocomplete.FutureModelForm, CommonForm):
    """Intervention form"""
    geomfields = ['_geom']

    target = autocomplete.Select2GenericForeignKeyModelField(
        model_choice=[
            (Station, 'label',),
            (Knowledge, 'name')
        ],
        label=_('Target'),
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
            "width",
            "height",
        )]

    class Meta:
        model = Intervention
        fields = [
            "structure", "target", "name", "date",
            "intervention_status", "intervention_type",
            "stake", "disorders", "description",
            "width", "height", "_geom"
        ]
        widgets = {
            'date': DatePickerInput(),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper.form_tag = False
