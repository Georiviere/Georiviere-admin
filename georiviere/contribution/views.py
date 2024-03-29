from mapentity.views import (MapEntityList, MapEntityDetail, MapEntityFormat, MapEntityLayer, MapEntityJsonList,
                             MapEntityUpdate, MapEntityDelete)


from georiviere.contribution.filters import ContributionFilterSet
from georiviere.contribution.forms import ContributionForm
from georiviere.contribution.models import Contribution


class ContributionList(MapEntityList):
    queryset = Contribution.objects.all()
    filterform = ContributionFilterSet
    columns = ['id', 'category', 'date_observation', 'severity', 'published']


class ContributionLayer(MapEntityLayer):
    queryset = Contribution.objects.all()
    model = Contribution
    filterform = ContributionFilterSet
    columns = ['category', ]


class ContributionJsonList(MapEntityJsonList, ContributionList):
    pass


class ContributionDetail(MapEntityDetail):
    model = Contribution


class ContributionFormat(MapEntityFormat, ContributionList):
    model = Contribution


class ContributionUpdate(MapEntityUpdate):
    model = Contribution
    form_class = ContributionForm


class ContributionDelete(MapEntityDelete):
    model = Contribution
