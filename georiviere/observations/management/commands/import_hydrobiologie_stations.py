from datetime import datetime
import json
import requests
from django.contrib.gis.geos import Point
from georiviere.observations.models import Station, StationProfile, Parameter, ParameterTracking, Unit
from . import BaseImportCommand


class Command(BaseImportCommand):
    help = "Import hydro-biological quality stations from Hub'Eau API"

    api_url = "https://hubeau.eaufrance.fr/api/v1/hydrobio/stations_hydrobio"
    api_analyse_taxons = "https://hubeau.eaufrance.fr/api/v1/hydrobio/taxons"
    api_analyse_indices = "https://hubeau.eaufrance.fr/api/v1/hydrobio/indices"

    def create_or_update_stations(self, results, verbosity, with_parameters=False):
        """Create or update stations from results"""
        station_profile, station_profile_created = StationProfile.objects.get_or_create(
            code='HYDROB'
        )
        if verbosity >= 2:
            if station_profile_created:
                self.stdout.write('Created station profile {0}'.format(station_profile))
        today = datetime.today().strftime('%d-%m-%Y')
        for station in results:
            operations_uri = f"{self.operations_url}?debut=01-01-1990&fin={today}&stations={station['code_station_hydrobio']}"
            station_obj, station_created = Station.objects.update_or_create(
                code=station['code_station_hydrobio'],
                defaults={
                    'label': station['libelle_station_hydrobio'] or "",
                    'station_uri': station['uri_station_hydrobio'] or "",
                    'geom': Point(
                        station['coordonnee_x'],
                        station['coordonnee_y'],
                        srid='2154'
                    ),
                    'operations_uri': operations_uri
                }
            )
            station_obj.save()
            station_obj.station_profiles.add(station_profile)

            if verbosity >= 2:
                if station_created:
                    self.stdout.write('Created station {0}'.format(station_obj))
                else:
                    self.stdout.write('Updated station {0}'.format(station_obj))

            if with_parameters:
                # Get 50 first and 50 last parameters from analyse_pc API endpoint
                payload_indices = {
                    'format': 'json',
                    'size': 50,
                    'code_station': station_obj.code,
                }
                try:
                    response_firstpage = requests.get(self.api_analyse_indices, params=payload_indices)
                except requests.exceptions.ConnectionError as e:
                    self.stdout.write(f'Limit of connection has been exceeded {e}')
                    continue
                try:
                    response_firstpage_content = response_firstpage.json()
                except json.JSONDecodeError:
                    self.stdout.write('Response is not a json')
                    continue
                indices_data = response_firstpage_content['data']

                for indice in indices_data:
                    # Create Unit for indices
                    unit_obj, unit_created = Unit.objects.get_or_create(
                        code=indice['code_indice'],
                        defaults={
                            'label': indice['unite_indice'],
                            'symbol': indice['unite_indice'],
                        }
                    )
                    if verbosity >= 2 and unit_created:
                        self.stdout.write('Added parameter {0}'.format(unit_obj))
                payload_taxons = {
                    'format': 'json',
                    'size': 50,
                    'code_station': station_obj.code,
                }
                response_firstpage = requests.get(self.api_analyse_taxons, params=payload_taxons)
                response_firstpage_content = response_firstpage.json()
                taxons_data = response_firstpage_content['data']

                for taxon in taxons_data:
                    codes_unit = taxon['codes_indices_operation']
                    unit = None
                    if codes_unit:
                        code_unit = codes_unit[0]
                        unit = Unit.objects.get(code=code_unit)
                    parameter_obj, parameter_created = Parameter.objects.get_or_create(
                        code=taxon['code_appel_taxon'],
                        defaults={
                            'label': taxon['libelle_appel_taxon'],
                            'unit': unit,
                            'parameter_type': Parameter.ParameterTypeChoice.QUALITATIVE,
                        }
                    )
                    parameter_tracking, parameter_tracking_created = ParameterTracking.objects.get_or_create(
                        station=station_obj,
                        parameter=parameter_obj,
                        defaults={
                            'label': taxon['libelle_appel_taxon'],
                            'measure_frequency': "",
                            'transmission_frequency': "",
                            'data_availability': ParameterTracking.DataAvailabilityChoice.ONLINE,
                        }
                    )

                    # Set start and end measure date
                    measure_date = datetime.strptime(taxon['date_prelevement'], '%Y-%m-%dT%H:%M:%SZ').date()

                    if not parameter_tracking.measure_start_date or parameter_tracking.measure_start_date > measure_date:
                        parameter_tracking.measure_start_date = measure_date

                    if not parameter_tracking.measure_end_date or parameter_tracking.measure_end_date < measure_date:
                        parameter_tracking.measure_end_date = measure_date

                    parameter_tracking.save()

                    if verbosity >= 2 and parameter_tracking_created:
                        self.stdout.write('Added parameter {0}'.format(parameter_tracking))
