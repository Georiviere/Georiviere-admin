import functools
import operator

from django.db.models import Q
from django_filters import MultipleChoiceFilter
from django.utils.translation import gettext_lazy as _
from mapentity.filters import MapEntityFilterSet, PythonPolygonFilter
from geotrek.zoning.filters import ZoningFilterSet

from georiviere.contribution.models import (
    Contribution, ContributionQuantity, ContributionQuality, ContributionFaunaFlora, ContributionLandscapeElements,
    ContributionPotentialDamage
)

from georiviere.watershed.filters import WatershedFilterSet


class ContributionCategoryFilter(MultipleChoiceFilter):
    def __init__(self, *args, **kwargs):
        self.choices = [
            ('potential_damage', _('Potential damage')),
            ('fauna_flora', _('Fauna flora')),
            ('quality', _('Quality')),
            ('quantity', _('Quantity')),
            ('landscape_element', _('Landscape elements')),
        ]
        super().__init__(choices=self.choices, *args, **kwargs)

    def filter(self, qs, values):
        if not values:
            return qs
        qs = qs.filter(functools.reduce(operator.or_, [Q(**{f'{value}__isnull': False}) for value in values]))
        return qs


class ContributionTypeFilter(MultipleChoiceFilter):
    choices_category = {}

    def __init__(self, *args, **kwargs):
        self.choices_category = {
            ContributionQuantity: {value: key for key, value in ContributionQuantity.TypeChoice.choices},
            ContributionQuality: {value: key for key, value in ContributionQuality.TypeChoice.choices},
            ContributionFaunaFlora: {value: key for key, value in ContributionFaunaFlora.TypeChoice.choices},
            ContributionLandscapeElements: {value: key for key, value in ContributionLandscapeElements.TypeChoice.choices},
            ContributionPotentialDamage: {value: key for key, value in ContributionPotentialDamage.TypeChoice.choices},
        }
        choices = ContributionQuantity.TypeChoice.labels + \
            ContributionQuality.TypeChoice.labels + \
            ContributionFaunaFlora.TypeChoice.labels + \
            ContributionLandscapeElements.TypeChoice.labels + \
            ContributionPotentialDamage.TypeChoice.labels
        self.choices = [(value, value) for value in choices]
        super().__init__(choices=self.choices, *args, **kwargs)

    def filter(self, qs, values):
        if not values:
            return qs
        contributions = []
        for key_model, dict_value in self.choices_category.items():
            contributions.extend(list(key_model.objects.filter(type__in=[dict_value.get(i) for i in values if dict_value.get(i) is not None]).values_list('contribution_id', flat=True)))
        qs = qs.filter(id__in=contributions)
        return qs


class ContributionFilterSet(WatershedFilterSet, ZoningFilterSet, MapEntityFilterSet):
    bbox = PythonPolygonFilter(field_name='geom')
    category_contribution = ContributionCategoryFilter(label=_('Category'))
    type_contribution = ContributionTypeFilter(label=_('Type'))

    class Meta(MapEntityFilterSet.Meta):
        model = Contribution
        fields = MapEntityFilterSet.Meta.fields + [
            "category_contribution", "type_contribution"
        ]
