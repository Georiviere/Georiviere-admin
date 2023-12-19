from django.conf import settings
from django.contrib.gis.db import models
from django.utils.translation import gettext_lazy as _

from georiviere.altimetry import AltimetryMixin
from geotrek.authent.models import StructureRelated, StructureOrNoneRelated
from geotrek.common.mixins import TimeStampedModelMixin
from geotrek.zoning.mixins import ZoningPropertiesMixin

from mapentity.models import MapEntityMixin
from georiviere.main.models import AddPropertyBufferMixin
from georiviere.watershed.mixins import WatershedPropertiesMixin


class EventType(StructureOrNoneRelated):
    name = models.CharField(max_length=128, verbose_name=_("Name"), )

    class Meta:
        verbose_name = _("Event type")
        verbose_name_plural = _("Event types")

    def __str__(self):
        return self.name


class Proceeding(AltimetryMixin, TimeStampedModelMixin, WatershedPropertiesMixin,
                 ZoningPropertiesMixin, AddPropertyBufferMixin, StructureRelated, MapEntityMixin):
    name = models.CharField(max_length=128, verbose_name=_("Name"), )
    date = models.DateField(blank=True, null=True, verbose_name=_("Date"))
    eid = models.CharField(verbose_name=_("External id"), max_length=1024, blank=True, null=True)
    description = models.TextField(blank=True, default="", verbose_name=_("Description"))
    geom = models.GeometryField(srid=settings.SRID, spatial_index=True)
    events_verbose_name = _("Events")

    def __str__(self):
        return '%s :  %s' % (self.name, self.date)

    @property
    def name_display(self):
        return '<a data-pk="%s" href="%s" title="%s">%s</a>' % (self.pk,
                                                                self.get_detail_url(),
                                                                self.name,
                                                                self.name)

    @classmethod
    def get_create_label(cls):
        return _("Add a new proceeding")

    class Meta:
        verbose_name = _("Proceeding")
        verbose_name_plural = _("Proceedings")
        triggers = AltimetryMixin.Meta.triggers


class Event(models.Model):
    proceeding = models.ForeignKey(
        Proceeding,
        related_name='events',
        verbose_name=_("Proceeding"),
        on_delete=models.CASCADE
    )

    event_type = models.ForeignKey(
        EventType,
        verbose_name=_("Event type"),
        on_delete=models.PROTECT
    )

    date = models.DateField(blank=True, null=True, verbose_name=_("Date"))

    def __str__(self):
        return '%s :  %s' % (self.event_type, self.date)

    class Meta:
        verbose_name = _("Event")
        verbose_name_plural = _("Events")
