from factory import django, Sequence, SubFactory
from georiviere.tests.factories import BaseLineStringFactory


from proceeding import models


class ProceedingFactory(BaseLineStringFactory):
    class Meta:
        model = models.Proceeding

    date = '2002-02-20'
    name = Sequence(lambda n: "Proceeding %s" % n)
    eid = Sequence(lambda n: "%s" % n)
    description = Sequence(lambda n: "Description %s" % n)


class EventTypeFactory(django.DjangoModelFactory):
    class Meta:
        model = models.EventType

    name = Sequence(lambda n: "Event type %s" % n)


class EventFactory(django.DjangoModelFactory):
    class Meta:
        model = models.Event

    event_type = SubFactory(EventTypeFactory)
    proceeding = SubFactory(ProceedingFactory)
    date = '2002-02-20'
