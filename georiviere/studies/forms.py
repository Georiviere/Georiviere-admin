from geotrek.common.forms import CommonForm

from georiviere.studies.models import Study
from georiviere.river.fields import SnappedGeometryField


class StudyForm(CommonForm):
    """Study form"""
    geom = SnappedGeometryField()

    geomfields = ['geom']

    class Meta(CommonForm.Meta):
        model = Study
        fields = "__all__"
