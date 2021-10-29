from mapentity import views as mapentity_views
from geotrek.authent.decorators import same_structure_required

from georiviere.studies.filters import StudyFilterSet
from georiviere.studies.forms import StudyForm
from georiviere.studies.models import Study


class StudyList(mapentity_views.MapEntityList):
    model = Study
    filterform = StudyFilterSet
    columns = ['id', 'title', 'year', 'study_types']


class StudyLayer(mapentity_views.MapEntityLayer):
    model = Study
    columns = ['title', 'year']


class StudyJsonList(mapentity_views.MapEntityJsonList, StudyList):
    pass


class StudyFormat(mapentity_views.MapEntityFormat, StudyList):
    model = Study


class StudyDocument(mapentity_views.MapEntityDocument):
    model = Study


class StudyDetail(mapentity_views.MapEntityDetail):
    model = Study

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['can_edit'] = self.get_object().same_structure(self.request.user)
        return context


class StudyCreate(mapentity_views.MapEntityCreate):
    model = Study
    form_class = StudyForm


class StudyUpdate(mapentity_views.MapEntityUpdate):
    model = Study
    form_class = StudyForm

    @same_structure_required('studies:study_detail')
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)


class StudyDelete(mapentity_views.MapEntityDelete):
    model = Study

    @same_structure_required('studies:study_detail')
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)
