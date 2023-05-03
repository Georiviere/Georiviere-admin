from django import template
import json
from georiviere.valorization.models import POICategory


register = template.Library()


@register.simple_tag
def all_poitypes():
    types = {
        str(poi_category.pk): list(poi_category.types.values_list('pk', flat=True))
        for poi_category in POICategory.objects.prefetch_related('types')
    }
    return json.dumps(types)
