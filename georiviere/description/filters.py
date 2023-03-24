from mapentity.filters import MapEntityFilterSet
from geotrek.zoning.filters import ZoningFilterSet

from georiviere.description.models import Usage, Land, Morphology, Status
from georiviere.river.filters import TopologyFilterSet
from georiviere.watershed.filters import WatershedFilterSet


class UsageFilterSet(WatershedFilterSet, ZoningFilterSet, MapEntityFilterSet):

    class Meta(MapEntityFilterSet.Meta):
        model = Usage
        fields = MapEntityFilterSet.Meta.fields + ['usage_types', ]


class LandFilterSet(WatershedFilterSet, ZoningFilterSet, MapEntityFilterSet):

    class Meta(MapEntityFilterSet.Meta):
        model = Land
        fields = MapEntityFilterSet.Meta.fields + ['land_type', 'control_type']


class MorphologyFilterSet(WatershedFilterSet, ZoningFilterSet, TopologyFilterSet,
                          MapEntityFilterSet):

    class Meta(MapEntityFilterSet.Meta):
        model = Morphology
        fields = MapEntityFilterSet.Meta.fields + ['good_working_space_left', 'good_working_space_right',
                                                   'facies_diversity', 'main_flow', 'secondary_flows',
                                                   'granulometric_diversity', 'full_edge_height', 'full_edge_width',
                                                   'sediment_dynamic', 'bank_state_left', 'bank_state_right',
                                                   'habitats_diversity', 'main_habitat', 'secondary_habitats',
                                                   'plan_layout']


class StatusFilterSet(WatershedFilterSet, ZoningFilterSet, TopologyFilterSet,
                      MapEntityFilterSet):

    class Meta(MapEntityFilterSet.Meta):
        model = Status
        fields = MapEntityFilterSet.Meta.fields + ['status_types', ]
