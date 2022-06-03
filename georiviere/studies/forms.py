from crispy_forms.layout import Div, Field
from geotrek.common.forms import CommonForm

from georiviere.studies.models import Study
from georiviere.river.fields import SnappedGeometryField


class StudyForm(CommonForm):
    """Study form"""
    geom = SnappedGeometryField()

    geomfields = ['geom']

    fieldslayout = [
        Div(
            'structure',
            'title',
            Field('study_types', css_class="chzn-select"),
            'year',
            'study_authors',
            'description',
        )
    ]

    class Meta:
        model = Study
        fields = "__all__"
