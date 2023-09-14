from django.contrib.gis.geos import Point
from georiviere.observations.models import Station, StationProfile
from . import BaseImportCommand


class Command(BaseImportCommand):
    help = "Import hydrometry stations from Hub'Eau API"
    api_url = "https://hubeau.eaufrance.fr/api/v1/hydrometrie/referentiel/stations"
    operations_url = " https://www.hydro.eaufrance.fr/sitehydro/"

    def create_or_update_stations(self, results, verbosity, with_parameters=False):
        """Create or update stations from results"""
        station_profile, station_profile_created = StationProfile.objects.get_or_create(
            code='HYDRO'
        )
        if verbosity >= 2:
            if station_profile_created:
                self.stdout.write('Created station profile {0}'.format(station_profile))

        for station in results:
            # uri_station is not in API data, so format id from code_station
            uri_station = "https://id.eaufrance.fr/StationHydro/{}".format(
                station['code_station'],
            ) or ""
            operations_uri = f"{self.operations_url}{station['code_site']}/series"
            station_obj, station_created = Station.objects.update_or_create(
                code=station['code_station'],
                defaults={
                    'label': station['libelle_station'] or "",
                    'site_code': station['code_site'] or "",
                    'purpose_code': station['code_finalite_station'] or "",
                    'description': station['descriptif_station'] or "",
                    'station_uri': uri_station,
                    'in_service': station['en_service'] or None,
                    'geom': Point(
                        station['coordonnee_x_station'],
                        station['coordonnee_y_station'],
                        srid='2154'
                    ),
                    'operations_uri': operations_uri,
                    'local_influence': station['influence_locale_station'] or Station.LocalInfluenceChoices.UNKNOWN,
                }
            )

            station_obj.station_profiles.add(station_profile)

            if verbosity >= 2:
                if station_created:
                    self.stdout.write('Created station {0}'.format(station_obj))
                else:
                    self.stdout.write('Updated station {0}'.format(station_obj))
