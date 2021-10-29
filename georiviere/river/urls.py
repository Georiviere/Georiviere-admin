from django.urls import path, register_converter, converters
from geotrek.altimetry.urls import AltimetryEntityOptions

from georiviere.river.views import CutTopologyView
from georiviere.river.models import Stream
from mapentity.registry import registry


class LangConverter(converters.StringConverter):
    # TODO: move this on geotrek to work with
    regex = '[a-z]{2}'


register_converter(LangConverter, 'lang')


app_name = 'river'


class StreamEntityOptions(AltimetryEntityOptions):
    pass


urlpatterns = [path('cut_topology/', CutTopologyView.as_view(), name='cut_topology'), ]
urlpatterns += registry.register(Stream, StreamEntityOptions)
