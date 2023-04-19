from django.contrib.gis.forms.fields import PointField

from crispy_forms.layout import Div, Field

from geotrek.common.forms import CommonForm

from georiviere.valorization.models import POIAction, POIKnowledge


class POIKnowledgeForm(CommonForm):
    geom = PointField()

    geomfields = ['geom']

    fieldslayout = [
        Div(
            'name',
            'description',
            'type',
            Field('portals', css_class="chzn-select"),
        )
    ]

    class Meta:
        model = POIKnowledge
        fields = ['name', 'description', 'type', 'portals', 'geom']


class POIActionForm(CommonForm):
    geom = PointField()

    geomfields = ['geom']

    fieldslayout = [
        Div(
            'name',
            'description',
            'type',
            Field('portals', css_class="chzn-select"),
        )
    ]

    class Meta:
        model = POIAction
        fields = ['name', 'description', 'type', 'portals', 'geom']
