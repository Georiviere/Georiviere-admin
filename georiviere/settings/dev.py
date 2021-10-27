from . import *  # NOQA

DEBUG = True
ALLOWED_HOSTS = ['*']

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

INSTALLED_APPS.append('debug_toolbar')

MIDDLEWARE += (
    'debug_toolbar.middleware.DebugToolbarMiddleware',
)

DEBUG_TOOLBAR_CONFIG = {
    'SHOW_TOOLBAR_CALLBACK': lambda x: True,
}

AUTH_PASSWORD_VALIDATORS = []
