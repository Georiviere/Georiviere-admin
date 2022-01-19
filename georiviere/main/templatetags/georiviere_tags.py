from django import template
from mapentity.helpers import alphabet_enumeration

register = template.Library()


@register.inclusion_tag('main/_detail_valuelist_source_fragment.html')
def valuelist_source(items, stream, field=None, enumeration=False):
    """
    Template tag to show a list of values in detail pages,
    with distance to stream source
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
        distance_to_source = stream.distance_to_source(item)
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
def valuelist_streams(streams, element):
    """
    Template tag to show a list of stream with object distance to source in detail pages.
    """
    valuelist = []
    for stream in streams:
        distance_to_source = stream.distance_to_source(element)
        valuelist.append({
            'pk': stream.pk,
            'text': stream.name_display,
            'distance_to_source': distance_to_source,
        })

    return {
        'valuelist': valuelist,
        'modelname': 'stream'
    }
