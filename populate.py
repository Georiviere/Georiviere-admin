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
    OfflineKnowledgeAttrs,
    OfflineKnowledgeGeom,
    OfflineFollowupAttrs,
    OfflineFollowupGeom,
)


def get_random_point():
    min_lon = 840_000
    max_lon = 958_000
    lon = randint(min_lon, max_lon)
    min_lat = 6_546_000
    max_lat = 6_661_000
    lat = randint(min_lat, max_lat)
    return Point(float(lon), float(lat), srid=2154)


def get_random_linestring(delta=(-50, 50)):
    first_point = get_random_point()
    next_point = Point(
        first_point.x + randint(*delta),
        first_point.y + randint(*delta),
        srid=2154
    )
    last_point = Point(
        next_point.x + randint(*delta),
        next_point.y + randint(*delta),
        srid=2154
    )
    return LineString(first_point, next_point, last_point)


def get_random_polygon():
    linestring = get_random_linestring(delta=(0, 500))
    coords = list(linestring.coords)
    print(coords)
    coords.append(coords[0])
    print(coords)
    return Polygon(coords)

# Création connaissances

for i in range(100):
    print(f"Création connaissance ponctuelle #{i}")
    k = OfflineKnowledgeAttrs(
        uuid=uuid4(),
        name=faker.text(max_nb_chars=20)
    )
    k.save()
    geom = OfflineKnowledgeGeom(
        uuid=uuid4(),
        geom=get_random_point(),
        knowledge_attrs_uuid=k.uuid
    )
    geom.save()
    print("Fait")

for i in range(100):
    print(f"Création connaissance linéaire #{i}")
    k = OfflineKnowledgeAttrs(
        uuid=uuid4(),
        name=faker.text(max_nb_chars=20)
    )
    k.save()
    geom = OfflineKnowledgeGeom(
        uuid=uuid4(),
        geom=get_random_linestring(),
        knowledge_attrs_uuid=k.uuid
    )
    geom.save()
    print("Fait")

for i in range(100):
    print(f"Création connaissance polygone #{i}")
    k = OfflineKnowledgeAttrs(
        uuid=uuid4(),
        name=faker.text(max_nb_chars=20)
    )
    k.save()
    geom = OfflineKnowledgeGeom(
        uuid=uuid4(),
        geom=get_random_polygon(),
        knowledge_attrs_uuid=k.uuid
    )
    geom.save()
    print("Fait")


# Création suivis

for i in range(100):
    print(f"Création suivi ponctuel #{i}")
    k = OfflineFollowupAttrs(
        uuid=uuid4(),
        name=faker.text(max_nb_chars=20)
    )
    k.save()
    geom = OfflineFollowupGeom(
        uuid=uuid4(),
        geom=get_random_point(),
        followup_attrs_uuid=k.uuid
    )
    geom.save()
    print("Fait")

for i in range(100):
    print(f"Création suivi linéaire #{i}")
    k = OfflineFollowupAttrs(
        uuid=uuid4(),
        name=faker.text(max_nb_chars=20)
    )
    k.save()
    geom = OfflineFollowupGeom(
        uuid=uuid4(),
        geom=get_random_linestring(),
        followup_attrs_uuid=k.uuid
    )
    geom.save()
    print("Fait")

for i in range(100):
    print(f"Création suivi polygone #{i}")
    k = OfflineFollowupAttrs(
        uuid=uuid4(),
        name=faker.text(max_nb_chars=20)
    )
    k.save()
    geom = OfflineFollowupGeom(
        uuid=uuid4(),
        geom=get_random_polygon(),
        followup_attrs_uuid=k.uuid
    )
    geom.save()
    print("Fait")
