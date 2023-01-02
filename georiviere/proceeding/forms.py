from django import forms

from django.forms.models import inlineformset_factory
from django.utils.translation import gettext_lazy as _

from crispy_forms.bootstrap import Tab, TabHolder
from crispy_forms.layout import Div
from crispy_forms.layout import Layout, Fieldset
from crispy_forms.helper import FormHelper

from georiviere.main.forms import CommonForm

from georiviere.main.widgets import DatePickerInput
from georiviere.proceeding.models import Proceeding, Event
from georiviere.river.fields import SnappedGeometryField


class EventForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.layout = Layout('id', 'event_type', 'date', )

    class Meta:
        fields = ['id', 'event_type', 'date']
        widgets = {
            'date': DatePickerInput(),
        }

    def save(self, *args, **kwargs):
        return super().save(*args, **kwargs)


EventFormSet = inlineformset_factory(Proceeding, Event, form=EventForm, extra=1)


class ProceedingForm(CommonForm):
    geom = SnappedGeometryField()

    geomfields = ['geom']

    fieldslayout = [
        Div(
            TabHolder(
                Tab(
                    _('Main fields'),
                    'structure',
                    'name',
                    'date',
                    'eid',
                    'description'
                ),
                Tab(
                    _('Events'),
                    Fieldset(_('Events')),
                )
            )
        )
    ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper.form_tag = False

    class Meta:
        model = Proceeding
        fields = ['id', 'name', 'geom', 'date', 'eid', 'description', 'structure']
        widgets = {
            'date': DatePickerInput(),
        }
