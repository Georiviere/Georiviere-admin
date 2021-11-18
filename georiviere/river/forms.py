from copy import deepcopy

from django import forms
from django.contrib.gis.geos import Point

from geotrek.common.forms import CommonForm

from georiviere.river.fields import SnappedLineStringField
from georiviere.river.models import Stream, Topology


class StreamForm(CommonForm):
    geom = SnappedLineStringField()

    geomfields = ['geom']

    class Meta(CommonForm):
        fields = "__all__"
        model = Stream

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fieldslayout = deepcopy(self.fieldslayout)
        self.fields['source_location'].label = ''
        self.fields['source_location'].widget.target_map = 'geom'
        self.fields['source_location'].widget.geometry_field_class = 'SourceLocationField'


class TopologyRiverForm(CommonForm):
    class Media:
        js = ('river/js/remove_delete_button.js', )


class CutTopologyForm(forms.Form):
    topology = forms.ModelChoiceField(queryset=Topology.objects.all(), widget=forms.widgets.HiddenInput())
    lat = forms.FloatField(widget=forms.HiddenInput())
    lng = forms.FloatField(widget=forms.HiddenInput())
