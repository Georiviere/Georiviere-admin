from django import template
from mapentity.helpers import alphabet_enumeration

register = template.Library()


@register.inclusion_tag('main/_detail_valuelist_source_fragment.html')
def valuelist_source(items, field=None, enumeration=False):
    """
    Common template tag to show a list of values in detail pages.

    :param field: Use this attribute on each item instead of their unicode representation
    :param enumeration: Show enumerations, useful to match those shown by ``mapentity/leaflet.enumeration.js``

    See https://github.com/makinacorpus/django-mapentity/issues/35
        https://github.com/makinacorpus/Geotrek/issues/960
        https://github.com/makinacorpus/Geotrek/issues/214
        https://github.com/makinacorpus/Geotrek/issues/871
    """
    if field:
        def display(v):
            return getattr(v, '%s_display' % field, getattr(v, field))
        itemslist = [display(v) for v in items]
    else:
        itemslist = items

    letters = alphabet_enumeration(len(items))

    valuelist = []
    for i, item in enumerate(itemslist):
        distance_to_source = None
        if hasattr(i, 'distance_to_source'):
            distance_to_source = 42
        valuelist.append({
            'enumeration': letters[i] if enumeration else False,
            'pk': getattr(items[i], 'pk', None),
            'text': item,
            'distance_to_source': distance_to_source,
        })

    modelname = None
    if len(items) > 0:
        oneitem = items[0]
        if hasattr(oneitem, '_meta'):
            modelname = oneitem._meta.object_name.lower()

    return {
        'valuelist': valuelist,
        'modelname': modelname
    }
