from crispy_forms.layout import Div, Field
from dal import autocomplete
from django.utils.translation import gettext_lazy as _

from geotrek.common.forms import CommonForm

from georiviere.contribution.models import Contribution
from georiviere.knowledge.models import FollowUp, Knowledge
from georiviere.maintenance.models import Intervention


class ContributionForm(autocomplete.FutureModelForm, CommonForm):
    geomfields = ['geom']

    linked_object = autocomplete.Select2GenericForeignKeyModelField(
        model_choice=[
            # Get the values 'name' for each object of each models
            (Knowledge, 'name'),
            (Intervention, 'name'),
            (FollowUp, 'name')
        ],
        label=_('Linked object'),
        required=False,
        initial=None,
    )

    fieldslayout = [
        Div(
            "description",
            "severity",
            "published",
            "validated",
            "portal",
            "email_author",
            "assigned_user",
            "status_contribution",
            Field('linked_object', css_class="chosen-select"),
        )
    ]

    class Meta(CommonForm):
        fields = ["description", "severity", "published", "portal", "email_author", "geom", "assigned_user",
                  "status_contribution", "validated", "linked_object"]
        model = Contribution

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['portal'].widget.attrs['readonly'] = True
        self.fields['geom'].widget.modifiable = False
        self.fields['email_author'].widget.attrs['readonly'] = True

    def clean_portal(self):
        return self.instance.portal

    def clean_linked_object(self):
        linked_object = self.cleaned_data['linked_object']
        if linked_object == "":
            return None
        return linked_object
