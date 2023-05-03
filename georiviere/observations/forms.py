from django.core.exceptions import ValidationError
from django.forms import inlineformset_factory, ModelForm, ModelChoiceField
from django.utils.translation import gettext_lazy as _
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Div, Field, Fieldset, Layout
from crispy_forms.bootstrap import Tab, TabHolder
from geotrek.common.forms import CommonForm

from georiviere.finances_administration.models import AdministrativeFile
from georiviere.main.widgets import DatePickerInput
from georiviere.river.fields import SnappedGeometryField

from .models import Station, ParameterTracking


class ParameterTrackingForm(ModelForm):

    class Meta:
        fields = (
            'id',
            'structure',
            'label',
            'station',
            'parameter',
            'measure_frequency',
            'transmission_frequency',
            'data_availability',
            'measure_start_date',
            'measure_end_date',
        )
        widgets = {
            'measure_start_date': DatePickerInput(),
            'measure_end_date': DatePickerInput(),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.layout = Layout(
            'id',
            'structure',
            'label',
            Field('parameter', css_class="chosen-select"),
            'measure_frequency',
            'transmission_frequency',
            'data_availability',
            'measure_start_date',
            'measure_end_date'
        )

    def save(self, *args, **kwargs):
        return super().save(*args, **kwargs)


ParameterTrackingFormset = inlineformset_factory(
    Station,
    ParameterTracking,
    form=ParameterTrackingForm,
    extra=1
)


class StationForm(CommonForm):
    """Station form"""
    geom = SnappedGeometryField()
    administrative_file = ModelChoiceField(label=_("Create operation on"), queryset=AdministrativeFile.objects.all(),
                                           required=False, initial=None)

    geomfields = ['geom']

    fieldslayout = [
        Div(
            TabHolder(
                Tab(
                    _('Main fields'),
                    'structure',
                    'code',
                    'label',
                    'description',
                    'station_uri',
                    'operations_uri',
                    'annex_uri',
                    'site_code',
                    'purpose_code',
                    'in_service',
                    'station_profiles',
                    Div(css_id="div_id_operations", css_class="form-group row"),
                    "administrative_file",
                ),
                Tab(
                    _('Parameters tracking'),
                    Fieldset(_('Parameters tracking')),
                )
            )
        )
    ]

    class Meta:
        model = Station
        fields = "__all__"
        help_texts = {
            'station_profiles': _('Hold Ctrl key to select multiple items'),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper.form_tag = False

    def clean_code(self):
        """If not unique raise error"""
        code = self.cleaned_data['code']
        qs = Station.objects.filter(code=code)
        if self.instance:
            qs = qs.exclude(pk=self.instance.id)
        if qs.count() > 0:
            raise ValidationError(_('This code is already in use.'))
        return code
