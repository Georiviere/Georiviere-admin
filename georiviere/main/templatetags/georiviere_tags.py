from django import template
from mapentity.helpers import alphabet_enumeration

register = template.Library()


@register.inclusion_tag('main/_detail_valuelist_source_fragment.html')
def valuelist_source(items, stream, field=None, enumeration=False):
    """
    Common template tag to show a list of values in detail pages.

    :param field: Use this attribute on each item instead of their unicode representation
    :param enumeration: Show enumerations, useful to match those shown by ``mapentity/leaflet.enumeration.js``

    See https://github.com/makinacorpus/django-mapentity/issues/35
        https://github.com/makinacorpus/Geotrek/issues/960
        https://github.com/makinacorpus/Geotrek/issues/214
        https://github.com/makinacorpus/Geotrek/issues/871
    """
    letters = alphabet_enumeration(len(items))

    modelname = None
    if len(items) > 0:
        oneitem = items[0]
        if hasattr(oneitem, '_meta'):
            modelname = oneitem._meta.object_name.lower()

    valuelist = []
    for i, item in enumerate(items):
        if field:
            text = getattr(item, '%s_display' % field, getattr(item, field))
        else:
            text = item
        distance_to_source = stream.distance_to_source
        valuelist.append({
            'enumeration': letters[i] if enumeration else False,
            'pk': getattr(items[i], 'pk', None),
            'text': text,
            'distance_to_source': distance_to_source,
        })

    return {
        'valuelist': valuelist,
        'modelname': modelname
    }


@register.inclusion_tag('main/_detail_valuelist_streams_fragment.html')
def valuelist_streams(streams, object):
    """
    Template tag to show a list of stream with object distance to source in detail pages.
    """
    valuelist = []
    for stream in streams:
        distance_to_source = stream.distance_to_source
        valuelist.append({
            'pk': stream.pk,
            'text': stream.name_display,
            'distance_to_source': distance_to_source,
        })

    return {
        'valuelist': valuelist,
        'modelname': 'stream'
    }
