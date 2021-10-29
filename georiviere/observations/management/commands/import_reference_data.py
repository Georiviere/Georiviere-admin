import requests

from django.core.management.base import BaseCommand

from georiviere.observations.models import Unit


class Command(BaseCommand):
    help = "Import reference data as unit and parameters"
    urf_url = "https://api.sandre.eaufrance.fr/referentiels/v1/urf.json"
    parameters_url = "https://api.sandre.eaufrance.fr/referentiels/v1/par.json?outputSchema=SANDREv4"

    def create_or_update_stations(self, results, verbosity):
        """Create or update stations from results"""
        raise NotImplementedError()

    def handle(self, *args, **options):
        """Import stations from API Hub'eau"""
        verbosity = options.get('verbosity')

        response = requests.get(self.urf_url)
        if verbosity >= 2:
            self.stdout.write('Get reference unit from API {0}'.format(response.url))

        response_content = response.json()
        urf_dataset = response_content['REFERENTIELS']['Referentiel']['UniteReference']

        if verbosity >= 1:
            self.stdout.write('Import {1} units from API {0}'.format(response.url, len(urf_dataset)))

        for urf in urf_dataset:
            unit, created = Unit.objects.get_or_create(
                code=urf['CdUniteReference'],
                defaults={
                    'label': urf['LbUniteReference'],
                    'symbol': urf['SymUniteReference'],
                }
            )

            if verbosity >= 2:
                if created:
                    self.stdout.write('Created unit {0}'.format(unit))
                else:
                    self.stdout.write('Updated unit {0}'.format(unit))
