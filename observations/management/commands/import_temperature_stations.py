from django.contrib.gis.geos import Point
from observations.models import Station, StationProfile, Parameter, ParameterTracking, Unit
from . import BaseImportCommand


class Command(BaseImportCommand):
    help = "Import hydrometry stations from Hub'Eau API"
    api_url = "https://hubeau.eaufrance.fr/api/v1/temperature/station"

    def create_or_update_stations(self, results, verbosity, with_parameters=False):
        """Create or update stations from results"""
        station_profile, station_profile_created = StationProfile.objects.get_or_create(
            code='TEMP'
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
                    )
                }
            )
            station_obj.station_profiles.add(station_profile)

            if verbosity >= 2:
                if station_created:
                    self.stdout.write('Created station {0}'.format(station_obj))
                else:
                    self.stdout.write('Updated station {0}'.format(station_obj))

            if with_parameters:
                # Create Parameter and Unit for temperature
                unit_obj, unit_created = Unit.objects.get_or_create(
                    code="27",
                    defaults={
                        'label': "degré Celsius",
                        'symbol': "°C",
                    }
                )
                parameter_obj, parameter_created = Parameter.objects.get_or_create(
                    code="1301",
                    defaults={
                        'label': "Température de l'Eau",
                        'unit': unit_obj,
                    }
                )
                parameter_tracking = ParameterTracking.objects.create(
                    label="Chronique température",
                    station=station_obj,
                    parameter=parameter_obj,
                    measure_frequency="",
                    transmission_frequency="",
                    data_availability=ParameterTracking.DataAvailabilityChoice.ONLINE,
                )

                if verbosity >= 2:
                    self.stdout.write('Added parameter {0}'.format(parameter_tracking))
