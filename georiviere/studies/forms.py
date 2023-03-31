from django.forms import ModelChoiceField
from django.utils.translation import gettext_lazy as _

from crispy_forms.layout import Div, Field
from geotrek.common.forms import CommonForm

from georiviere.finances_administration.models import AdministrativeFile
from georiviere.studies.models import Study
from georiviere.river.fields import SnappedGeometryField


class StudyForm(CommonForm):
    """Study form"""
    geom = SnappedGeometryField()
    administrative_file = ModelChoiceField(label=_("Create operation on"), queryset=AdministrativeFile.objects.all(),
                                           required=False, initial=None)

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
