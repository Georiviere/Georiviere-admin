import requests
from django.contrib.gis.geos import Point
from observations.models import Station, StationProfile, Parameter, ParameterTracking, Unit
from . import BaseImportCommand


class Command(BaseImportCommand):
    help = "Import physico-chemical quality stations from Hub'Eau API"
    api_url = "https://hubeau.eaufrance.fr/api/v1/qualite_rivieres/station_pc"
    api_analyse_pc_url = "https://hubeau.eaufrance.fr/api/v1/qualite_rivieres/analyse_pc"

    def create_or_update_stations(self, results, verbosity, with_parameters=False):
        """Create or update stations from results"""
        station_profile, station_profile_created = StationProfile.objects.get_or_create(
            code='PCQUAL'
        )
        if verbosity >= 2:
            if station_profile_created:
                self.stdout.write('Created station profile {0}'.format(station_profile))

        for station in results:
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
                }
            )
            station_obj.station_profiles.add(station_profile)

            if verbosity >= 2:
                if station_created:
                    self.stdout.write('Created station {0}'.format(station_obj))
                else:
                    self.stdout.write('Updated station {0}'.format(station_obj))

            if with_parameters:
                # Get parameters from analyse_pc API endpoint
                payload = {
                    'format': 'json',
                    'size': 50,
                    'code_station': station_obj.code,
                }
                response = requests.get(self.api_analyse_pc_url, params=payload)
                response_content = response.json()
                analysepc_data = response_content['data']

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
                            'data_availability': ParameterTracking.DataAvailabilityChoice.ONLINE,
                        }
                    )

                    if verbosity >= 2 and parameter_tracking_created:
                        self.stdout.write('Added parameter {0}'.format(parameter_tracking))
