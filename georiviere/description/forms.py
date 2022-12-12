from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from crispy_forms.layout import Field
from crispy_forms.bootstrap import AppendedText

from geotrek.common.forms import CommonForm

from georiviere.description.models import Land, Status, Morphology, Usage

from georiviere.river.forms import TopologyRiverForm
from georiviere.river.fields import SnappedGeometryField


class UsageForm(CommonForm):
    geom = SnappedGeometryField()

    fieldslayout = [
        'structure',
        Field('usage_types', css_class="chosen-select"),
        'description',
    ]

    geomfields = ['geom']

    class Meta:
        fields = "__all__"
        model = Usage


class LandForm(CommonForm):
    geom = SnappedGeometryField()

    geomfields = ['geom']

    class Meta:
        fields = "__all__"
        model = Land


class StatusForm(TopologyRiverForm):
    geomfields = ['geom']
    qualified = forms.BooleanField(
        label=_("Qualified"),
        required=False,
    )

    class Meta:
        fields = ['status_types', 'qualified', 'geom']
        model = Status
        help_texts = {
            'status_types': _('Hold Ctrl key to select multiple items'),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['qualified'].initial = self.instance.topology.qualified
        if self.instance:
            self.fields['qualified'].initial = True
        self.fields['geom'].widget.modifiable = False

    def clean(self):
        if self.cleaned_data.get('qualified') and not self.cleaned_data.get('status_types'):
            raise ValidationError(
                _("Status cannot be qualified but without type")
            )
        return self.cleaned_data

    def save(self, commit=True):
        self.instance.topology.qualified = self.cleaned_data['qualified']
        self.instance.topology.save()
        return super().save(commit=True)


class MorphologyForm(TopologyRiverForm):

    fieldslayout = [
        "good_working_space_left", "good_working_space_right",
        "facies_diversity", "main_flow",
        Field('secondary_flows', css_class="chzn-select"),
        "granulometric_diversity",
        AppendedText("full_edge_height", "m"),
        AppendedText("full_edge_width", "m"),
        "sediment_dynamic",
        "bank_state_left", "bank_state_right",
        "habitats_diversity", "main_habitat",
        Field('secondary_habitats', css_class="chzn-select"),
        "plan_layout", "qualified"
    ]
    geomfields = ['geom']
    qualified = forms.BooleanField(required=False)

    class Meta:
        fields = ["good_working_space_left", "good_working_space_right", "facies_diversity", "main_flow",
                  "secondary_flows", "granulometric_diversity", "full_edge_height", "full_edge_width", "sediment_dynamic",
                  "bank_state_left", "bank_state_right", "habitats_diversity", "main_habitat", "secondary_habitats",
                  "plan_layout", "geom", "qualified", ]
        model = Morphology

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['qualified'].initial = self.instance.topology.qualified
        if self.instance:
            self.fields['qualified'].initial = True
        self.fields['geom'].widget.modifiable = False

    def save(self, commit=True):
        self.instance.topology.qualified = self.cleaned_data['qualified']
        self.instance.topology.save()
        return super().save(commit=True)
