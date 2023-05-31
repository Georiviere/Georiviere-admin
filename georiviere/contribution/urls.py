from .models import Contribution
from mapentity.registry import MapEntityOptions, registry


class ContributionOptions(MapEntityOptions):
    dynamic_views = ['List', 'JsonList', 'Layer', 'Detail', 'Update']


app_name = 'contribution'
urlpatterns = registry.register(Contribution, options=ContributionOptions, menu=True)
