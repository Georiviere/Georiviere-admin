import json
import requests

from django.core.management.base import BaseCommand, CommandError


class BaseImportCommand(BaseCommand):
    help = "Import whatever stations from Hub'Eau API"
    api_url = ""
    operations_url = "https://naiades.eaufrance.fr/acces-donnees#/physicochimie/operations"

    def add_arguments(self, parser):
        parser.add_argument('--department', nargs='+', help="Department code")
        parser.add_argument('-p', '--with-parameters', action='store_true',
                            help="Get also parameter tracked by the station")
        parser.add_argument('--size', help="Results per page")

    def create_or_update_stations(self, *args, **kwargs):
        """Create or update stations from results"""
        raise NotImplementedError()

    def handle(self, *args, **options):
        """Import stations from API Hub'eau"""
        # Get args
        department = options.get('department')
        verbosity = options.get('verbosity')
        with_parameters = options.get('with_parameters')
        size = options.get('size')

        # Build query
        payload = {
            'format': 'json',
            'size': 1000,
        }
        if size:
            payload.update({'size': size})
        if department:
            payload.update({'code_departement': options['department']})

        response = requests.get(self.api_url, params=payload)

        if response.status_code not in [200, 206]:
            message = "Failed to fetch {}. Status code : {}.".format(
                self.api_url,
                response.status_code
            )
            raise CommandError(message)

        if verbosity >= 2:
            self.stdout.write('Get station from API {0}'.format(response.url))
        try:
            response_content = response.json()
        except json.decoder.JSONDecodeError:
            self.stdout.write('Response is not a json')
            return
        if verbosity >= 1:
            self.stdout.write('Import {1} stations from API {0}'.format(response.url, response_content['count']))

        # Update or create stations
        results = response_content['data']
        self.create_or_update_stations(results, verbosity, with_parameters)
        while response_content['next']:
            response = requests.get(response_content['next'])
            if verbosity >= 2:
                self.stdout.write('Import next page from {0}'.format(response.url))
            try:
                response_content = response.json()
            except requests.exceptions.JSONDecodeError:
                self.stdout.write('Response is not a json')
                return
            results = response_content['data']
            self.create_or_update_stations(results, verbosity, with_parameters)
