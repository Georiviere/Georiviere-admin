from mapentity.views import MapEntityList, MapEntityDetail, MapEntityFormat, MapEntityLayer, MapEntityJsonList


from georiviere.contribution.filters import ContributionFilterSet
from georiviere.contribution.models import Contribution


class ContributionList(MapEntityList):
    queryset = Contribution.objects.all()
    filterform = ContributionFilterSet
    columns = ['id', 'category', 'name_author', 'email_author',
               'date_observation', 'severity']


class ContributionLayer(MapEntityLayer):
    queryset = Contribution.objects.all()
    model = Contribution


class ContributionJsonList(MapEntityJsonList, ContributionList):
    pass


class ContributionDetail(MapEntityDetail):
    model = Contribution

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['can_edit'] = False
        return context


class ContributionFormat(MapEntityFormat, ContributionList):
    model = Contribution
