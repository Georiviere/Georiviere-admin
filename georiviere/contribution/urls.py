from .models import Contribution
from mapentity.registry import MapEntityOptions, registry


class ContributionOptions(MapEntityOptions):
    # Here we remove "Create" and "Delete" view of contributions. Contributions are only created with the portal.
    # TODO: Add a command wich allow to remove multiple contributions
    dynamic_views = ['List', 'JsonList', 'Layer', 'Detail', 'Update']


app_name = 'contribution'
urlpatterns = registry.register(Contribution, options=ContributionOptions, menu=True)
