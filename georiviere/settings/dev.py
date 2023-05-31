from . import *  # NOQA

# debug and allow all hosts
DEBUG = True
ALLOWED_HOSTS = ['*']

# mail send in django console
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

# Enable debug toolbar
INSTALLED_APPS.append('debug_toolbar')
INSTALLED_APPS.append('django_extensions')
INSTALLED_APPS.append('drf_yasg')

MIDDLEWARE += (
    'debug_toolbar.middleware.DebugToolbarMiddleware',
)

DEBUG_TOOLBAR_CONFIG = {
    'SHOW_TOOLBAR_CALLBACK': lambda x: True,
}

# No extra password validator
AUTH_PASSWORD_VALIDATORS = []

# Disable cache
MAPENTITY_CONFIG['GEOJSON_LAYERS_CACHE_BACKEND'] = 'default'

# Use postgis image template to make postgres/postgis extensions available in test database (postgres_raster)
DATABASES['default'].setdefault('TEST', {'TEMPLATE': 'template_postgis'})
