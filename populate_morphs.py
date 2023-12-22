import os
from uuid import uuid4

import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'georiviere.settings')
django.setup()

from georiviere.description.models import Morphology, OfflineMorphology


morphs = Morphology.objects.all()
for morph in morphs:
    print(f"Création offline morphology pour stream {morph.topology.stream.name}")
    om = OfflineMorphology(
        uuid=uuid4(),
        gra_id = morph.pk,
        stream_name=morph.topology.stream.name,
        geom=morph.geom,
        qualified=False,
        username="Bob",
    )
    om.save()
