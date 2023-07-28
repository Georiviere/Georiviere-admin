from django.template.loader import render_to_string

from geotrek.sensitivity.parsers import BiodivParser as GeotrekBiodivParser

from geotrek.common.parsers import RowImportError
from django.conf import settings
from django.contrib.gis.geos import Polygon
from geotrek.sensitivity.models import SportPractice


# TODO: We should remove this part of the parser with the latest version. Fix of this parser is in the version 2.77.3
class BiodivParser(GeotrekBiodivParser):
    def report(self, output_format='txt'):
        context = {
            'nb_success': self.nb_success,
            'nb_lines': self.line,
            'nb_created': self.nb_created,
            'nb_updated': self.nb_updated,
            'nb_deleted': len(self.to_delete) if self.delete else None,
            'nb_unmodified': self.nb_unmodified,
            'warnings': self.warnings,
        }
        return render_to_string('main/parser_report.{output_format}'.format(output_format=output_format), context)

    def next_row(self):
        response = self.request_or_retry('https://biodiv-sports.fr/api/v2/sportpractice/')
        for practice in response.json()['results']:
            defaults = {'name_' + lang: practice['name'][lang] for lang in practice['name'].keys() if
                        lang in settings.MODELTRANSLATION_LANGUAGES}
            SportPractice.objects.get_or_create(id=practice['id'], defaults=defaults)
        bbox = Polygon.from_bbox(settings.SPATIAL_EXTENT)
        bbox.srid = settings.SRID
        bbox.transform(4326)  # WGS84
        self.next_url = self.url
        while self.next_url:
            params = {
                'in_bbox': ','.join([str(coord) for coord in bbox.extent]),
            }
            if self.practices:
                params['practices'] = ','.join([str(practice) for practice in self.practices])
            response = self.request_or_retry(self.next_url, params=params)

            self.root = response.json()
            self.nb = int(self.root['count'])

            for row in self.items:
                yield row
            self.next_url = self.root['next']

    def filter_species(self, src, val):
        try:
            val = super().filter_species(src, val)
        except ValueError:
            raise RowImportError
        return val
