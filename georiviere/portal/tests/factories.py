from factory import django, Sequence

from .. import models


class PortalFactory(django.DjangoModelFactory):
    class Meta:
        model = models.Portal

    name = Sequence(lambda n: "Portal %s" % n)
    website = Sequence(lambda n: "https://georiviere-{}.fr".format(n))
