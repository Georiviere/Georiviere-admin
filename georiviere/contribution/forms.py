from crispy_forms.layout import Div

from django.conf import settings
from django.contrib.gis.forms.fields import PointField

from geotrek.common.forms import CommonForm

from georiviere.contribution.models import Contribution


class ContributionForm(CommonForm):
    can_delete = False
    geom = PointField(srid=settings.SRID)
    geomfields = ['geom']
    fieldslayout = [
        Div(
            "description",
            "severity",
            "published",
            "portal"
        )
    ]

    class Meta(CommonForm):
        fields = ["description", "severity", "published", "portal"]
        model = Contribution

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['portal'].widget.attrs['disabled'] = True
        self.fields['geom'].widget.modifiable = False
