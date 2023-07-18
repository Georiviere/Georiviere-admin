from datetime import datetime
import json
import requests
from django.contrib.gis.geos import Point
from georiviere.observations.models import Station, StationProfile, Parameter, ParameterTracking, Unit
from . import BaseImportCommand


class Command(BaseImportCommand):
    help = "Import physico-chemical quality stations from Hub'Eau API"
    api_url = "https://hubeau.eaufrance.fr/api/v2/qualite_rivieres/station_pc"
    api_analyse_pc_url = "https://hubeau.eaufrance.fr/api/v2/qualite_rivieres/analyse_pc"

    def create_or_update_stations(self, results, verbosity, with_parameters=False):
        """Create or update stations from results"""
        station_profile, station_profile_created = StationProfile.objects.get_or_create(
            code='PCQUAL'
        )
        if verbosity >= 2:
            if station_profile_created:
                self.stdout.write('Created station profile {0}'.format(station_profile))
        today = datetime.today().strftime('%d-%m-%Y')

        for station in results:
            operations_uri = f"{self.operations_url}?debut=01-01-1990&fin={today}&stations={station['code_station']}"
            station_obj, station_created = Station.objects.update_or_create(
                code=station['code_station'],
                defaults={
                    'label': station['libelle_station'] or "",
                    'station_uri': station['uri_station'] or "",
                    'geom': Point(
                        station['coordonnee_x'],
                        station['coordonnee_y'],
                        srid='2154'
                    ),
                    'hardness': station['durete'],
                    'operations_uri': operations_uri
                }
            )
            if station['date_arret']:
                station_obj.in_service = False
            else:
                station_obj.in_service = True
            station_obj.save()
            station_obj.station_profiles.add(station_profile)

            # Get data availability for this station (will be used in parameter_tracked)
            if station['nature'] == 'M':
                data_availability = ParameterTracking.DataAvailabilityChoice.ONDEMAND
            elif station['nature'] == 'A':
                data_availability = ParameterTracking.DataAvailabilityChoice.ONLINE

            if verbosity >= 2:
                if station_created:
                    self.stdout.write('Created station {0}'.format(station_obj))
                else:
                    self.stdout.write('Updated station {0}'.format(station_obj))

            if with_parameters:
                # Get 50 first and 50 last parameters from analyse_pc API endpoint
                payload = {
                    'format': 'json',
                    'size': 50,
                    'code_station': station_obj.code,
                }
                try:
                    response_firstpage = requests.get(self.api_analyse_pc_url, params=payload)
                except requests.exceptions.ConnectionError as e:
                    self.stdout.write(f'Limit of connection has been exceeded {e}')
                    continue
                try:
                    response_firstpage_content = response_firstpage.json()
                except json.JSONDecodeError:
                    self.stdout.write('Response is not a json')
                    continue
                analysepc_data = response_firstpage_content['data']

                # If there is more than one page, get data desc sorted
                if response_firstpage_content['count'] > 50:
                    payload['sort'] = 'desc'
                    try:
                        response_desc_results = requests.get(self.api_analyse_pc_url, params=payload)
                    except requests.exceptions.ConnectionError as e:
                        self.stdout.write(f'Limit of connection has been exceeded {e}')
                        continue
                    try:
                        response_desc_data = response_desc_results.json()['data']
                    except json.JSONDecodeError:
                        self.stdout.write('Response is not a json')
                        continue
                    analysepc_data = analysepc_data + response_desc_data

                for measure in analysepc_data:

                    # Create Parameter and Unit for temperature
                    unit_obj, unit_created = Unit.objects.get_or_create(
                        code=measure['code_unite'],
                        defaults={
                            'label': measure['symbole_unite'],
                            'symbol': measure['symbole_unite'],
                        }
                    )
                    parameter_obj, parameter_created = Parameter.objects.get_or_create(
                        code=measure['code_parametre'],
                        defaults={
                            'label': measure['libelle_parametre'],
                            'unit': unit_obj,
                        }
                    )
                    parameter_tracking, parameter_tracking_created = ParameterTracking.objects.get_or_create(
                        station=station_obj,
                        parameter=parameter_obj,
                        defaults={
                            'label': measure['libelle_parametre'],
                            'measure_frequency': "",
                            'transmission_frequency': "",
                            'data_availability': data_availability,
                        }
                    )

                    # Set start and end measure date
                    measure_date = datetime.strptime(measure['date_prelevement'], '%Y-%m-%d').date()

                    if not parameter_tracking.measure_start_date or parameter_tracking.measure_start_date > measure_date:
                        parameter_tracking.measure_start_date = measure_date

                    if not parameter_tracking.measure_end_date or parameter_tracking.measure_end_date < measure_date:
                        parameter_tracking.measure_end_date = measure_date

                    parameter_tracking.save()

                    if verbosity >= 2 and parameter_tracking_created:
                        self.stdout.write('Added parameter {0}'.format(parameter_tracking))
