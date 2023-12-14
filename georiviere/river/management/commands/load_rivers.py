from django.contrib.gis.gdal import DataSource
from django.contrib.gis.geos import Point
from django.core.management import BaseCommand
from django.utils.timezone import now
from django.utils.translation import gettext as _

from georiviere.description.models import Morphology, Status
from georiviere.river.models import Stream, Topology


class Command(BaseCommand):
    help = 'Load Rivers'

    def add_arguments(self, parser):
        parser.add_argument('file_path', help="File's path to import.")
        parser.add_argument('--name-attribute', '-n', action='store', dest='name', default='nom',
                            help="Name of the name's attribute inside the file")
        parser.add_argument('--flush-streams', '-f', action='store_true', dest='flush', default=False,
                            help="Flush current streams")
        parser.add_argument('--default-name-attribute', '-nd', action='store', dest='default_name', default=_('River'),
                            help="Default name to use if name is empty")

    def handle(self, *args, **options):
        file_path = options.get('file_path')
        name_column = options.get('name')
        default_name = options.get('default_name')
        flush = options.get('flush')
        data_source = DataSource(file_path)
        layer = data_source[0]
        total_count = len(layer)
        self.stdout.write(f"Load rivers: {total_count} features to import")
        count = 0
        if flush:
            self.stdout.write(f"Delete streams.....", ending="")
            Stream.objects.all().delete()
            self.stdout.write(self.style.SUCCESS("done!"))
        bulks = []
        for feat in layer:
            geom = feat.geom.geos
            bulks.append(Stream(geom=geom,
                   source_location=Point(geom[0]),
                   name=feat.get(name_column) or default_name))
            count += 1
            if len(bulks) == 100:
                objs = Stream.objects.bulk_create(bulks)
                # for obj in objs:
                #     topo = Topology.objects.create(start_position=0, end_position=1, stream=obj)
                #     Morphology.objects.create(topology=topo, geom=obj.geom)
                #     topo = Topology.objects.create(start_position=0, end_position=1, stream=obj)
                #     Status.objects.create(topology=topo, geom=obj.geom)

                bulks = []
                now_2 = now()
                self.stdout.write(f"{count} / {total_count}")

        self.stdout.write(f"Morpholgy creation")
