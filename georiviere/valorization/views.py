from mapentity import views as mapentity_views
from geotrek.authent.decorators import same_structure_required

from georiviere.valorization.filters import POIActionFilterSet, POIKnowledgeFilterSet
from georiviere.valorization.forms import POIActionForm, POIKnowledgeForm
from georiviere.valorization.models import POIAction, POIKnowledge


class POIKnowledgeList(mapentity_views.MapEntityList):
    model = POIKnowledge
    filterform = POIKnowledgeFilterSet
    columns = ['id', 'name', 'type']


class POIKnowledgeLayer(mapentity_views.MapEntityLayer):
    model = POIKnowledge
    columns = ['name', 'type']


class POIKnowledgeJsonList(mapentity_views.MapEntityJsonList, POIKnowledgeList):
    pass


class POIKnowledgeFormat(mapentity_views.MapEntityFormat, POIKnowledgeList):
    model = POIKnowledge


class POIKnowledgeDocument(mapentity_views.MapEntityDocument):
    model = POIKnowledge


class POIKnowledgeDetail(mapentity_views.MapEntityDetail):
    model = POIKnowledge

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['can_edit'] = self.get_object().same_structure(self.request.user)
        return context


class POIKnowledgeCreate(mapentity_views.MapEntityCreate):
    model = POIKnowledge
    form_class = POIKnowledgeForm


class POIKnowledgeUpdate(mapentity_views.MapEntityUpdate):
    model = POIKnowledge
    form_class = POIKnowledgeForm

    @same_structure_required('valorization:poiknowledge_detail')
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)


class POIKnowledgeDelete(mapentity_views.MapEntityDelete):
    model = POIKnowledge

    @same_structure_required('valorization:poiknowledge_detail')
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)


class POIActionList(mapentity_views.MapEntityList):
    model = POIAction
    filterform = POIActionFilterSet
    columns = ['id', 'name', 'type']


class POIActionLayer(mapentity_views.MapEntityLayer):
    model = POIAction
    columns = ['name', 'type']


class POIActionJsonList(mapentity_views.MapEntityJsonList, POIKnowledgeList):
    pass


class POIActionFormat(mapentity_views.MapEntityFormat, POIKnowledgeList):
    model = POIAction


class POIActionDocument(mapentity_views.MapEntityDocument):
    model = POIAction


class POIActionDetail(mapentity_views.MapEntityDetail):
    model = POIAction

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['can_edit'] = self.get_object().same_structure(self.request.user)
        return context


class POIActionCreate(mapentity_views.MapEntityCreate):
    model = POIAction
    form_class = POIActionForm


class POIActionUpdate(mapentity_views.MapEntityUpdate):
    model = POIAction
    form_class = POIActionForm

    @same_structure_required('valorization:poiaction_detail')
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)


class POIActionDelete(mapentity_views.MapEntityDelete):
    model = POIAction

    @same_structure_required('valorization:poiaction_detail')
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)
