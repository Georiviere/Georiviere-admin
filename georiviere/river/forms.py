from copy import deepcopy

from django import forms

from geotrek.common.forms import CommonForm

from georiviere.river.widgets import SourceLocationWidget
from georiviere.river.fields import SnappedLineStringField
from georiviere.river.models import Stream, Topology


class StreamForm(CommonForm):
    geom = SnappedLineStringField()

    geomfields = ['geom']

    class Meta(CommonForm):
        fields = "__all__"
        model = Stream
        widgets = {
            'source_location': SourceLocationWidget()
        }


class TopologyRiverForm(CommonForm):
    class Media:
        js = ('river/js/remove_delete_button.js', )


class CutTopologyForm(forms.Form):
    topology = forms.ModelChoiceField(queryset=Topology.objects.all(), widget=forms.widgets.HiddenInput())
    lat = forms.FloatField(widget=forms.HiddenInput())
    lng = forms.FloatField(widget=forms.HiddenInput())
