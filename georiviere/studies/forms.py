from crispy_forms.layout import Div, Field
from geotrek.common.forms import CommonForm

from georiviere.finances_administration.forms import AdministrativeFileObjectFormMixin
from georiviere.studies.models import Study
from georiviere.river.fields import SnappedGeometryField


class StudyForm(AdministrativeFileObjectFormMixin, CommonForm):
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
            Div(css_id="div_id_operations", css_class="form-group row"),
            "administrative_file",
        )
    ]

    class Meta:
        model = Study
        fields = "__all__"
