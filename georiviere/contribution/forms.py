from crispy_forms.layout import Div, Field
from dal import autocomplete
from django import forms
from django.utils.translation import gettext_lazy as _
from django_jsonform.forms.fields import JSONFormField
from geotrek.common.forms import CommonForm

from georiviere.knowledge.models import FollowUp, Knowledge
from georiviere.maintenance.models import Intervention

from . import models


class ContributionForm(autocomplete.FutureModelForm, CommonForm):
    geomfields = ["geom"]

    linked_object = autocomplete.Select2GenericForeignKeyModelField(
        model_choice=[
            # Get the values 'name' for each object of each models
            (Knowledge, "name"),
            (Intervention, "name"),
            (FollowUp, "name"),
        ],
        label=_("Linked object"),
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
            Field("linked_object", css_class="chosen-select"),
        )
    ]

    class Meta(CommonForm):
        fields = [
            "description",
            "severity",
            "published",
            "portal",
            "email_author",
            "geom",
            "assigned_user",
            "status_contribution",
            "validated",
            "linked_object",
        ]
        model = models.Contribution

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["portal"].widget.attrs["readonly"] = True
        self.fields["geom"].widget.modifiable = False
        self.fields["email_author"].widget.attrs["readonly"] = True

    def clean_portal(self):
        return self.instance.portal

    def clean_linked_object(self):
        linked_object = self.cleaned_data["linked_object"]
        if linked_object == "":
            return None
        return linked_object


class CustomContributionForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance.pk:
            schema = self.instance.custom_type.get_json_schema_form()
            self.fields["data"] = JSONFormField(schema=schema, label=_("Data"))

    class Meta:
        model = models.CustomContribution
        fields = "__all__"


class CustomContributionFieldForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance.pk:
            schema = self.instance.get_customization_json_schema_form()
            self.fields["customization"] = JSONFormField(
                schema=schema, required=False, label=_("Customization")
            )
            self.fields["value_type"].disabled = True
            self.fields["value_type"].help_text = _(
                "You can't change value type after creation. Delete and/or create another one."
            )

    class Meta:
        model = models.CustomContributionTypeField
        fields = (
            "custom_type",
            "label",
            "value_type",
            "required",
            "help_text",
            "customization",
        )
