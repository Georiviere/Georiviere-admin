from . import *  ## NOQA

SRID = 2154
DEFAULT_STRUCTURE_NAME = "My structure"

# SPATIAL_EXTENT = (879300, 6556100, 971400, 6651700)

# LEAFLET_CONFIG['SPATIAL_EXTENT'] = (0, 40, 10, 55)


LEAFLET_CONFIG['TILES'].append(
    ('Ortho',
     '//wxs.ign.fr/choisirgeoportail/wmts?LAYER=ORTHOIMAGERY.ORTHOPHOTOS&EXCEPTIONS=image/jpeg&FORMAT=image/jpeg&SERVICE=WMTS&VERSION=1.0.0&REQUEST=GetTile&STYLE=normal&TILEMATRIXSET=PM&TILEMATRIX={z}&TILEROW={y}&TILECOL={x}',
     '&copy; IGN - GeoPortail')
)

# Enable sentry

# import sentry_sdk
# import georiviere
#
# from sentry_sdk.integrations.django import DjangoIntegration
#
# sentry_sdk.init(
#     dsn=os.getenv('SENTRY_DSN'),
#     environment=os.getenv('SENTRY_ENVIRONMENT'),
#     integrations=[DjangoIntegration()],
#     # If you wish to associate users to errors (assuming you are using
#     # django.contrib.auth) you may enable sending PII data.
#     send_default_pii=True,
#     release=georiviere.__version__,
#     traces_sample_rate=0.2
# )
