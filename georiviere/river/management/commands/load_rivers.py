from itertools import islice

from django.contrib.gis.gdal import DataSource
from django.contrib.gis.geos import Point
from django.core.management import BaseCommand
from django.utils.translation import gettext as _

from georiviere.river.models import Stream


class Command(BaseCommand):
    help = 'Load Rivers'

    def add_arguments(self, parser):
        parser.add_argument('file_path', help="File's path to import.")
        parser.add_argument('--name-attribute', '-n', action='store', dest='name', default='nom',
                            help="Attribute name in file to use as river name")
        parser.add_argument('--flush-streams', '-f', action='store_true', dest='flush', default=False,
                            help="Flush current streams")
        parser.add_argument('--default-name-attribute', '-nd', action='store', dest='default_name', default=_('River'),
                            help="Default name to use if attribute name specified is empty")

    def handle(self, *args, **options):
        file_path = options.get('file_path')
        name_column = options.get('name')
        default_name = options.get('default_name')
        flush = options.get('flush')
        data_source = DataSource(file_path)
        layer = data_source[0]
        total_count = len(layer)
        self.stdout.write(f"Load rivers: {total_count} features to import")
        if flush:
            self.stdout.write("Delete streams.....", ending="")
            Stream.objects.all().delete()
            self.stdout.write(self.style.SUCCESS("done!"))

        batch_size = 100

        objs = (Stream(geom=feat.geom.geos,
                       source_location=Point(feat.geom.geos[0]),
                       name=feat.get(name_column) or default_name) for feat in layer)
        count = 0
        while True:
            batch = list(islice(objs, batch_size))
            count += len(batch)
            if not batch:
                break
            self.stdout.write(f"{count} / {total_count}", ending="")
            Stream.objects.bulk_create(batch, batch_size)
            self.stdout.write(self.style.SUCCESS(" ok!"))

        self.stdout.write(self.style.SUCCESS(f"Successfully import {total_count} rivers and associated morphologies / status"))
