import logging
from mapentity.views import (MapEntityLayer, MapEntityList, MapEntityJsonList, MapEntityFormat, MapEntityDocumentWeasyprint,
                             MapEntityDetail, MapEntityDocumentOdt, MapEntityCreate, MapEntityUpdate, MapEntityDelete)

from main.views import FormsetMixin
from proceeding.filters import ProceedingFilterSet
from proceeding.forms import EventFormSet, ProceedingForm
from proceeding.models import Proceeding

from geotrek.authent.decorators import same_structure_required


logger = logging.getLogger(__name__)


class EventMixin(FormsetMixin):
    context_name = 'event_formset'
    formset_class = EventFormSet


class ProceedingList(MapEntityList):
    model = Proceeding
    filterform = ProceedingFilterSet
    columns = ['id', 'name', 'date', 'eid']


class ProceedingLayer(MapEntityLayer):
    model = Proceeding
    properties = ['name', 'date', 'eid']


class ProceedingJsonList(MapEntityJsonList, ProceedingList):
    pass


class ProceedingFormat(MapEntityFormat, ProceedingList):
    model = Proceeding


class ProceedingDocumentOdt(MapEntityDocumentOdt):
    model = Proceeding


class ProceedingDocumentWeasyprint(MapEntityDocumentWeasyprint):
    model = Proceeding


class ProceedingDetail(MapEntityDetail):
    model = Proceeding

    def get_context_data(self, *args, **kwargs):
        context = super(ProceedingDetail, self).get_context_data(*args, **kwargs)
        context['can_edit'] = self.get_object().same_structure(self.request.user)
        return context


class ProceedingCreate(EventMixin, MapEntityCreate):
    model = Proceeding
    form_class = ProceedingForm


class ProceedingUpdate(EventMixin, MapEntityUpdate):
    model = Proceeding
    form_class = ProceedingForm

    @same_structure_required('proceeding:proceeding_detail')
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)


class ProceedingDelete(MapEntityDelete):
    model = Proceeding

    @same_structure_required('proceeding:proceeding_detail')
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)
