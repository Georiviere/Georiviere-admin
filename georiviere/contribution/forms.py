from crispy_forms.layout import Div

from geotrek.common.forms import CommonForm

from georiviere.contribution.models import Contribution


class ContributionForm(CommonForm):
    can_delete = False
    geomfields = ['geom']

    fieldslayout = [
        Div(
            "description",
            "severity",
            "published",
            "validated"
            "portal",
            "email_author",
            "assigned_user",
            "status_contribution",
        )
    ]

    class Meta(CommonForm):
        fields = ["description", "severity", "published", "portal", "email_author", "geom", "assigned_user",
                  "status_contribution", "validated"]
        model = Contribution

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['portal'].widget.attrs['readonly'] = True
        self.fields['geom'].widget.modifiable = False
        self.fields['email_author'].widget.attrs['readonly'] = True

    def clean_portal(self):
        return self.instance.portal
