"""
script pour générer des objets pour les tables tampons de GRA :

- knowledge_offlineknowledge
- knowledge_offlinefollowup
- maintenance_offlineintervention

Pour les 3 types de géométrie, pour 2 utilisateurs. Seuls certains champs reçoivent une valeur, le but
est de tester l'UI de QGIS/QField avec beaucoup d'objets. Ou de vérifier certaines hypothèses.

Pour exécuter :

    docker compose run --rm web /opt/venv/bin/python /opt/georiviere-admin/populate.py
"""

import os
from random import randint
from uuid import uuid4

import django
from django.contrib.gis.geos import Point, LineString, Polygon
from faker import Faker

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'georiviere.settings')
django.setup()
faker = Faker('fr_FR')

from georiviere.knowledge.models import (  # after django.setup()
    OfflineKnowledge,
    OfflineFollowup
)
from georiviere.maintenance.models import (
    OfflineIntervention,
)

linestring_relative_coords = [
    [-28, 5],
    [-55, -6],
    [-70, -20],
    [-73, -35],
    [-76, -62],
]

polygon_relative_coords = [
    [118, 229],
    [185, 37],
    [119, -44],
    [71, -66],
    [73, -114],
    [88, -6],
    [6, -156],
    [-100, -209],
    [-204, -47],
    [-181, 110],
    [-190, 90],
    [13, 176],
]


def get_random_point():
    min_lon = 840_000
    max_lon = 958_000
    lon = randint(min_lon, max_lon)
    min_lat = 6_546_000
    max_lat = 6_661_000
    lat = randint(min_lat, max_lat)
    return Point(float(lon), float(lat), srid=2154)


def get_random_linestring():
    from copy import copy
    origin = get_random_point()
    coords = []
    coords.append(copy(origin))
    prev = origin  # previous
    for rel_coord in linestring_relative_coords:
        next_point = Point(prev.x + rel_coord[0],
                           prev.y + rel_coord[1],
                           srid=2154)
        coords.append(next_point)
        prev = next_point
    return LineString(coords)


def get_random_polygon():
    from copy import copy
    origin = get_random_point()
    coords = []
    coords.append(copy(origin))
    prev = origin  # previous
    for rel_coord in polygon_relative_coords:
        next_point = Point(prev.x + rel_coord[0],
                           prev.y + rel_coord[1],
                           srid=2154)
        coords.append(next_point)
        prev = next_point
    coords.append(copy(origin))
    return Polygon(coords)


map = {
    "connaissance": OfflineKnowledge,
    "suivi": OfflineFollowup,
    "intervention": OfflineIntervention,
}

serial_counters = {
    "connaissance": 0,
    "suivi": 0,
    "intervention": 0,
}

usernames = ("Bob",)
object_quantity = 1000  # for each geom type and each model


def get_next_id(model_name):
    next_id = serial_counters[model_name]
    serial_counters[model_name] += 1
    return next_id


for model_name, model in map.items():

    for i in range(object_quantity):
        print(f"Création {model_name} ponctuelle #{i}")

        # Field values from GRA (common to all users)
        gra_id = get_next_id(model_name)
        geom = get_random_point()
        name = f"{model_name[:4]}. {faker.text(max_nb_chars=20)}"

        for username in usernames:
            k = model(
                uuid=uuid4(),  # uuid is user-specific,
                gra_id=gra_id,
                geom=geom,
                name=name,
                username=username,
            )
            k.save()
        print("Fait")

    for i in range(object_quantity):
        print(f"Création {model_name} linéaire #{i}")

        # Field values from GRA (common to all users)
        gra_id = get_next_id(model_name)
        geom = get_random_linestring()
        name = f"{model_name[:4]}. {faker.text(max_nb_chars=20)}"

        for username in usernames:
            k = model(
                uuid=uuid4(),  # uuid is user-specific,
                gra_id=gra_id,
                geom=geom,
                name=name,
                username=username,
            )
            k.save()
        print("Fait")

    for i in range(object_quantity):
        print(f"Création {model_name} polygone #{i}")

        # Field values from GRA (common to all users)
        gra_id = get_next_id(model_name)
        geom = get_random_polygon()
        name = f"{model_name[:4]}. {faker.text(max_nb_chars=20)}"

        for username in usernames:
            k = model(
                uuid=uuid4(),  # uuid is user-specific,
                geom=geom,
                name=name,
                username=username,
            )
            k.save()
        print("Fait")
