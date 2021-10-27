from mapentity.filters import MapEntityFilterSet

from description.models import Usage, Land, Morphology, Status
from main.filters import RestrictedAreaFilterSet
from river.filters import TopologyFilterSet
from watershed.filters import WatershedFilterSet

from geotrek.zoning.filters import ZoningFilterSet


class UsageFilterSet(WatershedFilterSet, RestrictedAreaFilterSet, ZoningFilterSet, MapEntityFilterSet):

    class Meta(MapEntityFilterSet.Meta):
        model = Usage
        fields = MapEntityFilterSet.Meta.fields + ['usage_types', ]


class LandFilterSet(WatershedFilterSet, RestrictedAreaFilterSet, ZoningFilterSet, MapEntityFilterSet):

    class Meta(MapEntityFilterSet.Meta):
        model = Land
        fields = MapEntityFilterSet.Meta.fields + ['land_type', ]


class MorphologyFilterSet(WatershedFilterSet, RestrictedAreaFilterSet, ZoningFilterSet, TopologyFilterSet,
                          MapEntityFilterSet):

    class Meta(MapEntityFilterSet.Meta):
        model = Morphology
        fields = MapEntityFilterSet.Meta.fields + ['good_working_space_left', 'good_working_space_right',
                                                   'facies_diversity', 'main_flow', 'secondary_flow',
                                                   'granulometric_diversity', 'full_edge_height', 'full_edge_width',
                                                   'sediment_dynamic', 'bank_state_left', 'bank_state_right',
                                                   'habitats_diversity', 'main_habitat', 'secondary_habitat',
                                                   'plan_layout']


class StatusFilterSet(WatershedFilterSet, RestrictedAreaFilterSet, ZoningFilterSet, TopologyFilterSet,
                      MapEntityFilterSet):

    class Meta(MapEntityFilterSet.Meta):
        model = Status
        fields = MapEntityFilterSet.Meta.fields + ['status_types', ]
