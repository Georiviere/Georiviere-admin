from mapentity import views as mapentity_views
from geotrek.authent.decorators import same_structure_required

from georiviere.valorization.filters import POIFilterSet
from georiviere.valorization.forms import POIForm
from georiviere.valorization.models import POI


class POIList(mapentity_views.MapEntityList):
    model = POI
    filterform = POIFilterSet
    columns = ['id', 'name', 'type']


class POILayer(mapentity_views.MapEntityLayer):
    model = POI
    columns = ['name', 'type']


class POIJsonList(mapentity_views.MapEntityJsonList, POIList):
    pass


class POIFormat(mapentity_views.MapEntityFormat, POIList):
    model = POI


class POIDocument(mapentity_views.MapEntityDocument):
    model = POI


class POIDetail(mapentity_views.MapEntityDetail):
    model = POI

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['can_edit'] = self.get_object().same_structure(self.request.user)
        return context


class POICreate(mapentity_views.MapEntityCreate):
    model = POI
    form_class = POIForm


class POIUpdate(mapentity_views.MapEntityUpdate):
    model = POI
    form_class = POIForm

    @same_structure_required('valorization:poi_detail')
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)


class POIKDelete(mapentity_views.MapEntityDelete):
    model = POI

    @same_structure_required('valorization:poi_detail')
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)
