from django.forms import inlineformset_factory, ModelForm, DecimalField
from django.utils.translation import gettext_lazy as _
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Div, HTML, Layout, Field, Button
from crispy_forms.bootstrap import AppendedText, Tab, TabHolder, FormActions
from dal import autocomplete
from mapentity.forms import SubmitButton
from geotrek.common.forms import CommonForm

from georiviere.main.widgets import DatePickerInput
from georiviere.studies.models import Study
from georiviere.observations.models import Station
from georiviere.maintenance.models import Intervention
from georiviere.knowledge.models import FollowUp
from georiviere.finances_administration.models import AdministrativeFile, AdministrativeOperation, ManDay


class FundingForm(ModelForm):

    class Meta:
        fields = ('id', 'amount', 'organism')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.layout = Layout(
            'id',
            AppendedText('amount', '&euro;'),
            'organism'
        )


FundingFormSet = inlineformset_factory(
    AdministrativeFile,
    AdministrativeFile.funders.through,
    form=FundingForm,
    extra=1,
)


class AdministrativeOperationForm(autocomplete.FutureModelForm):

    content_object = autocomplete.Select2GenericForeignKeyModelField(
        model_choice=[
            (Station, 'label',),
            (Study, 'title'),
            (Intervention, 'name'),
            (FollowUp, 'name'),
        ],
        label=_('Operation on'),
    )
    manday_cost = DecimalField(
        label=_("Cost of man-day"),
        disabled=True,
        required=False,
        help_text=_("Man-day cost (read-only)")
    )

    class Meta:
        model = AdministrativeOperation
        fields = (
            'id', 'name', 'content_object', 'operation_status',
            'estimated_cost', 'material_cost', 'subcontract_cost',
            'manday_cost'
        )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.layout = Layout(
            'id',
            'name',
            Field('content_object', css_class="chosen-select"),
            'operation_status',
            HTML('<div class="w-100"></div>'),
            AppendedText('estimated_cost', '&euro;'),
            AppendedText('material_cost', '&euro;'),
            AppendedText('subcontract_cost', '&euro;'),
            AppendedText('manday_cost', '&euro;'),
        )

    def save(self, *args, **kwargs):
        return super().save(*args, **kwargs)


AdministrativeOperationFormset = inlineformset_factory(
    AdministrativeFile,
    AdministrativeOperation,
    form=AdministrativeOperationForm,
    extra=1,
)


class AdministrativeOperationCostsForm(ModelForm):

    class Meta:
        model = AdministrativeOperation
        fields = (
            'id', 'name', 'operation_status',
            'estimated_cost', 'material_cost', 'subcontract_cost',
        )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False

        actions = [
            Button('cancel', _('Cancel'), css_class="btn btn-light ml-auto mr-2"),
            SubmitButton('save_changes', _('Save changes')),
        ]
        formactions = FormActions(
            *actions,
            css_class="form-actions",
            template='mapentity/crispy_forms/bootstrap4/layout/formactions.html'
        )

        self.helper.layout = Layout(
            'id',
            'name',
            'operation_status',
            AppendedText('estimated_cost', '&euro;'),
            AppendedText('material_cost', '&euro;'),
            AppendedText('subcontract_cost', '&euro;'),
            Div(css_id="mandayWrapper"),
            formactions,
        )


class ManDayForm(ModelForm):

    class Meta:
        fields = ('id', 'nb_days', 'job_category')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.layout = Layout(
            'id',
            'nb_days',
            'job_category',
        )


ManDayFormSet = inlineformset_factory(
    AdministrativeOperation,
    ManDay,
    form=ManDayForm,
    extra=1,
)


class AdministrativeFileForm(CommonForm):
    """AdministrativeFile form"""

    fieldslayout = [
        Div(
            TabHolder(
                Tab(
                    _('General information'),
                    'structure',
                    'name',
                    'begin_date',
                    'end_date',
                    'description',
                    'adminfile_type',
                    'domain',
                    'constraints'
                ),
                Tab(
                    _('Stakeholders'),
                    'project_owners',
                    'project_managers',
                    'contractors'
                ),
                Tab(
                    _('Financing'),
                    Div(css_id="fundingWrapper"),
                ),
                Tab(
                    _('Operations'),
                    AppendedText('global_cost', '&euro;'),
                    Div(css_id="adminoperationWrapper"),
                )
            )
        )
    ]

    class Meta(CommonForm.Meta):
        model = AdministrativeFile
        fields = CommonForm.Meta.fields + [
            'structure', 'name', 'begin_date', 'end_date',
            'description', 'adminfile_type', 'domain',
            'constraints', 'global_cost',
            'project_owners', 'project_managers', 'contractors'
        ]
        widgets = {
            'begin_date': DatePickerInput(),
            'end_date': DatePickerInput(),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper.form_tag = False
