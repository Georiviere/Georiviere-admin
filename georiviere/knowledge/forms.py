from django.forms import ModelForm
from django.utils.translation import gettext_lazy as _

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Div, Fieldset
from crispy_forms.bootstrap import AppendedText
from geotrek.common.forms import CommonForm

from georiviere.knowledge.models import Knowledge, Vegetation, Work, FollowUp
from georiviere.main.widgets import DatePickerInput
from georiviere.river.fields import SnappedGeometryField


class KnowledgeForm(CommonForm):
    """Knowledge form"""
    geom = SnappedGeometryField()

    geomfields = ['geom']

    fieldslayout = [
        Div(
            'structure',
            'name',
            'code',
            'description',
            'knowledge_type',
            Fieldset(
                _('Vegetation details'),
                css_id="vegetationFieldset",
                css_class="d-none",
            ),
            Fieldset(
                _('Work details'),
                css_id="workFieldset",
                css_class="d-none",
            ),
        )
    ]

    class Meta(CommonForm.Meta):
        model = Knowledge
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper.form_tag = False


class VegetationForm(ModelForm):
    """Vegetation form, to be included in Knowledge form"""

    class Meta:
        model = Vegetation
        exclude = ["knowledge"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-md-auto'
        self.helper.field_class = 'controls col-md-auto'


class WorkForm(ModelForm):
    """Work form, to be included in Knowledge form"""

    fieldslayout = Layout(
        "work_type",
        "material",
        "state",
        "downstream_bank_effect",
        "upstream_bank_effect",
        "downstream_influence",
        "upstream_influence",
        "sediment_effect",
        "fish_continuity_effect",
        "usage",
        AppendedText("width", "m"),
        AppendedText("height", "m"),
        AppendedText("length", "m"),
        AppendedText("drop_height", "m"),
        "filling",
    )

    class Meta:
        model = Work
        exclude = ["knowledge"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.layout = self.fieldslayout
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-md-auto'
        self.helper.field_class = 'controls col-md-auto'


class FollowUpForm(CommonForm):
    """FollowUp form"""
    _geom = SnappedGeometryField(required=False)

    geomfields = ['_geom']

    fieldslayout = [
        Div(
            "structure",
            "name",
            "date",
            "followup_type",
            "knowledge",
            AppendedText("length", "m"),
            AppendedText("width", "m"),
            AppendedText("height", "m"),
            "measure_frequency",
            "description",
        )]

    class Meta:
        model = FollowUp
        fields = [
            "structure", "name", "date", "followup_type", "knowledge",
            "length", "width", "height", "measure_frequency", "description", "_geom"
        ]
        widgets = {
            'date': DatePickerInput(),
        }

    def __init__(self, knowledge=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper.form_tag = False
        if not self.instance.pk:
            # New followup, set its knowledge from knowledge_id
            if knowledge:
                self.fields['knowledge'].initial = knowledge
                self.helper.form_action += '?knowledge_id={}'.format(knowledge.id)
