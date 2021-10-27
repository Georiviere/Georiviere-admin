import json

from django import template
from django.contrib.gis.db.models import Extent
from django.contrib.gis.db.models.functions import Envelope, Transform
from django.conf import settings
from django.urls import reverse

from watershed.models import WatershedType, Watershed


register = template.Library()


def get_bbox_watersheds(watershed_type):
    return Watershed.objects.filter(watershed_type=watershed_type).annotate(extent=Extent(Transform(Envelope('geom'), settings.API_SRID))).\
        values_list('name', 'extent').order_by('name')


@register.inclusion_tag('watershed/_bbox_fragment_watershed.html')
def combobox_bbox_watershed():
    serialized = {}
    types_watershed = Watershed.objects.select_related('watershed_type').values_list('watershed_type', flat=True)
    used_types = WatershedType.objects.filter(pk__in=types_watershed)
    for watershed_type in used_types:
        serialized[watershed_type.pk] = [watershed_type.name, get_bbox_watersheds(watershed_type)]
    print(serialized)
    return {
        'bbox_watersheds': serialized
    }


@register.simple_tag
def watershed_types():
    all_used_types = Watershed.objects.values_list('watershed_type', flat=True)
    used_types = WatershedType.objects.filter(pk__in=all_used_types)
    serialized = []
    for watershed_type in used_types:
        watershed_type_url = reverse('watershed:watershed_type_layer',
                                     kwargs={'type_pk': watershed_type.pk})
        serialized.append({
            'id': 'watershed',
            'name': watershed_type.name,
            'url': watershed_type_url,
            'color': watershed_type.color
        })
    return json.dumps(serialized)
