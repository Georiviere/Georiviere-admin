from django.conf import settings
from django.contrib import messages
from django.contrib.gis.db.models.functions import Distance
from django.contrib.gis.geos import Point
from django.contrib.gis.db.models.functions import Length, LineLocatePoint
from django.core.exceptions import PermissionDenied
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import F, FloatField, Case, Min, When
from django.db.utils import InternalError
from django.http import JsonResponse
from django.http.response import HttpResponseRedirect
from django.utils.translation import gettext as _
from django.views.generic.edit import FormView
from django.views.generic.base import View
from geotrek.authent.decorators import same_structure_required

from georiviere.functions import ClosestPoint, LineSubString
from georiviere.main.decorators import same_structure_required_with_fallback
from .forms import CutTopologyForm, StreamForm
from .models import Stream, Topology
from .filters import StreamFilterSet

from mapentity import views as mapentity_views


class StreamList(mapentity_views.MapEntityList):
    queryset = Stream.objects.all()
    columns = ['id', 'name', 'length']
    filterform = StreamFilterSet


class StreamLayer(mapentity_views.MapEntityLayer):
    queryset = Stream.objects.select_related('classification_water_policy')


class StreamJsonList(mapentity_views.MapEntityJsonList, StreamList):
    pass


class StreamFormat(mapentity_views.MapEntityFormat):
    queryset = Stream.objects.all()


class StreamDocumentOdt(mapentity_views.MapEntityDocumentOdt):
    queryset = Stream.objects.all()


class StreamDocumentWeasyprint(mapentity_views.MapEntityDocumentWeasyprint):
    queryset = Stream.objects.all()


class StreamDetail(mapentity_views.MapEntityDetail):
    queryset = Stream.objects.all()

    @property
    def icon_sizes(self):
        return {
            'source': settings.ICON_SIZES['river_source'],
        }

    def get_context_data(self, *args, **kwargs):
        context = super(StreamDetail, self).get_context_data(*args, **kwargs)
        context['can_edit'] = self.get_object().same_structure(self.request.user)
        return context


class StreamCreate(mapentity_views.MapEntityCreate):
    model = Stream
    form_class = StreamForm


class StreamUpdate(mapentity_views.MapEntityUpdate):
    model = Stream
    form_class = StreamForm

    @same_structure_required('river:stream_detail')
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)


class StreamDelete(mapentity_views.MapEntityDelete):
    model = Stream

    @same_structure_required('river:stream_detail')
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)


class TopologyUpdateMixin(object):
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['can_delete'] = False
        return kwargs


class TopologyListMixin(object):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['can_add'] = False
        return context


class TopologyAddDeleteMixin(object):
    def dispatch(self, *args, **kwargs):
        raise PermissionDenied


class CutTopologyView(LoginRequiredMixin, FormView):
    form_class = CutTopologyForm
    http_method_names = ['post']

    @same_structure_required_with_fallback('river:stream_detail', 'river:stream_list')
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def form_valid(self, form):
        topology = form.cleaned_data['topology']
        if hasattr(topology, 'status'):
            instance = topology.status
        elif hasattr(topology, 'morphology'):
            instance = topology.morphology
        try:

            geom_point = Point(x=float(form.cleaned_data['lng']),
                               y=float(form.cleaned_data['lat']),
                               srid=4326).transform(settings.SRID, clone=True)
            topology_filter = instance.__class__.objects.filter(pk=instance.pk).annotate(locate_point=LineLocatePoint('geom', geom_point))
            locate_point = topology_filter.first().locate_point
            if locate_point == 0 or locate_point == 1:
                messages.error(self.request, _("Topology could not be cut"))
                return HttpResponseRedirect(instance.__class__.get_detail_url(instance))
        except InternalError:
            messages.error(self.request, _("Topology could not be cut"))
            return HttpResponseRedirect(instance.__class__.get_detail_url(instance))
        old_start_position = topology.start_position
        old_end_position = topology.end_position
        final_position = (old_end_position - old_start_position) * locate_point + old_start_position
        topology.start_position = final_position
        topology.save()

        new_topology = Topology.objects.create(start_position=old_start_position, end_position=final_position,
                                               stream=topology.stream)

        duplicate_instance = instance
        duplicate_instance.pk = None
        duplicate_instance.topology = new_topology
        duplicate_instance.save()
        new_topology.save()

        messages.success(self.request, _("Topology has been cut"))
        return HttpResponseRedirect(duplicate_instance.get_detail_url())


class DistanceToSourceView(LoginRequiredMixin, View):
    http_method_names = ['get']

    def get(self, request, *args, **kwargs):
        geom_point = Point(x=float(request.GET['lng_distance']),
                           y=float(request.GET['lat_distance']),
                           srid=4326).transform(settings.SRID, clone=True)
        streams = Stream.objects.annotate(distance=Distance(
            F('geom'), geom_point, output_field=FloatField()))
        stream_min_distance = streams.aggregate(
            min_distance=Min(F('distance'))
        )['min_distance']
        streams = streams.annotate(locate_source=LineLocatePoint(F('geom'),
                                                                 F('source_location')),
                                   locate_point=LineLocatePoint(F('geom'),
                                                                ClosestPoint(F('geom'),
                                                                             geom_point)),
                                   locate=Length(LineSubString(
                                       F('geom'),
                                       Case(
                                           When(locate_source__gte=F('locate_point'),
                                                then=F('locate_point')),
                                           default=F('locate_source')
                                       ),
                                       Case(
                                           When(locate_source__gte=F('locate_point'),
                                                then=F('locate_source')),
                                           default=F('locate_point')
                                       ))) + F('distance') + Distance(F('geom'),
                                                                      F('source_location'),
                                                                      output_field=FloatField())
                                   ).filter(distance=stream_min_distance)

        return JsonResponse({"distance": round(streams.first().locate, 1) if streams else 0})
