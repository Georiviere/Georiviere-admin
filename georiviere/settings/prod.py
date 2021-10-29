import sentry_sdk
import georiviere

from sentry_sdk.integrations.django import DjangoIntegration
from . import *  # NOQA
#
# MAIL SETTINGS
# ..........................
DEFAULT_FROM_EMAIL = os.getenv('SERVER_EMAIL', 'root@localhost')
# address will be set for sended emails (ex: noreply@yourdomain.net)
SERVER_EMAIL = DEFAULT_FROM_EMAIL

EMAIL_HOST = os.getenv('EMAIL_HOST', 'localhost')
EMAIL_HOST_USER = os.getenv('EMAIL_HOST_USER', '')
EMAIL_HOST_PASSWORD = os.getenv('EMAIL_HOST_PASSWORD', '')
EMAIL_PORT = os.getenv('EMAIL_HOST_PORT', 25)
EMAIL_USE_TLS = bool(os.getenv('EMAIL_USE_TLS', False))
EMAIL_USE_SSL = bool(os.getenv('EMAIL_USE_SSL', False))

# ADMINS = (
#     ('admin1', 'admin1@geotrek.fr'), # change with tuple ('your name', 'your@address.mail')
# )
# used to send error mails

# MANAGERS = (
#     ('manager1', 'manager1@geotrek.fr'), # change with tuple ('your name', 'your@address.mail')
# )

ALLOWED_HOSTS = os.getenv('DOMAIN_NAME').split(',')

sentry_sdk.init(
    dsn=os.getenv('SENTRY_DSN'),
    environment=os.getenv('SENTRY_ENVIRONMENT'),
    integrations=[DjangoIntegration()],
    # If you wish to associate users to errors (assuming you are using
    # django.contrib.auth) you may enable sending PII data.
    send_default_pii=True,
    release=georiviere.__version__,
    traces_sample_rate=0.2
)

# SECURITY
SECURE_CONTENT_TYPE_NOSNIFF = True
SECURE_BROWSER_XSS_FILTER = True
CSRF_COOKIE_HTTPONLY = True
CSRF_COOKIE_SECURE = True
SESSION_COOKIE_SECURE = True
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

PRIVATE_DIR = BASE_DIR.parent / "private"
CACHE_ROOT = os.path.join(PRIVATE_DIR, 'cache')

CACHES['fat'] = {
    'BACKEND': 'django.core.cache.backends.filebased.FileBasedCache',
    'LOCATION': CACHE_ROOT,
    'TIMEOUT': 28800,  # 8 hours
}

SESSION_ENGINE = "django.contrib.sessions.backends.cache"

MAPENTITY_CONFIG['GEOJSON_LAYERS_CACHE_BACKEND'] = 'fat'

# Public files
PUBLIC_DIR = os.path.join(BASE_DIR.parent, 'public')
STATIC_ROOT = os.path.join(PUBLIC_DIR, 'static')
MEDIA_ROOT = os.path.join(PUBLIC_DIR, 'media')
