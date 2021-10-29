from geotrek.common.forms import CommonForm

from georiviere.studies.models import Study


class StudyForm(CommonForm):
    """Study form"""
    geomfields = ['geom']

    class Meta(CommonForm.Meta):
        model = Study
        fields = "__all__"
