import shutil
from tempfile import TemporaryDirectory

from . import *  # NOQA


CACHES['default'] = {
    'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
    'LOCATION': 'default',
}
CACHES['fat'] = {
    'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
    'LOCATION': 'fat',
}

# recreate TMP_DIR for tests, and it as base dir forl all files
TMP_DIR = os.path.join(TMP_DIR, 'tests')
if os.path.exists(TMP_DIR):
    shutil.rmtree(TMP_DIR)
else:
    os.makedirs(TMP_DIR)
SESSIONS_DIR = os.path.join(TMP_DIR, 'sessions')
os.makedirs(SESSIONS_DIR)

SESSION_FILE_PATH = SESSIONS_DIR  # sessions files
MEDIA_ROOT = TemporaryDirectory(dir=TMP_DIR).name  # media files
# Use postgis image template to make postgres/postgis extensions available in test database (postgres_raster)
DATABASES['default'].setdefault('TEST', {'TEMPLATE': 'template_postgis'})
