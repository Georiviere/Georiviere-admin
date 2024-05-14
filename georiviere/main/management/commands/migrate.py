from django.apps import apps
from django.conf import settings
from django.contrib.gis.gdal import SpatialReference
from django.core.exceptions import ImproperlyConfigured
from django.core.management.commands.migrate import Command as BaseCommand
from django.core.management import call_command

from geotrek.common.utils.postgresql import load_sql_files


def check_srid_has_meter_unit():
    # TODO : move this on geotrek to work with
    if not hasattr(check_srid_has_meter_unit, '_checked'):
        if SpatialReference(settings.SRID).units[1] != 'metre':
            err_msg = 'Unit of SRID EPSG:%s is not meter.' % settings.SRID
            raise ImproperlyConfigured(err_msg)
    check_srid_has_meter_unit._checked = True


class Command(BaseCommand):
    def handle(self, *args, **options):
        check_srid_has_meter_unit()
        for app in apps.get_app_configs():
            load_sql_files(app, 'pre')
        super().handle(*args, **options)
        for app in apps.get_app_configs():
            try:
                load_sql_files(app, 'post')
            except Exception:  # NOQA
                pass
        call_command('sync_translation_fields', '--noinput')
        call_command('update_translation_fields')
